# SPEC: Notion Knowledge Assistant (Serverless Microservices RAG)

> Status: Draft v0.4 · Audience: AI coding agents and human reviewers
> This document is the source of truth. If code and spec disagree, the spec wins until the spec is amended in a reviewed change.
> Changes from v0.2: architecture is microservices (three domain services plus a platform stack), replacing the hexagonal layering. Infrastructure remains the Serverless Framework.
> Changes from v0.3: refined using an analysis of the legacy PoC code (section 10): page-level Notion traversal, chunk metadata, follow-up handling, provider defaults and an evaluation baseline.

---

## 1. Purpose

A personal assistant that answers natural-language questions using only the content of the owner's Notion workspace, and cites the pages it used.

**Goals**
- G1. Answer questions grounded in Notion content, with source citations.
- G2. Keep the index in sync with Notion with minimal manual work.
- G3. Be a reference implementation of a distributed serverless microservices system with explicit scalability paths and known limits (section 12).

**Non-goals (v1)**
- Multi-tenant / multi-user accounts, billing, or sharing.
- Writing back to Notion.
- Non-Notion sources (files, web, email).
- Fine-tuning models.
- Autonomous agent behaviour (tool use, actions). v1 is retrieval + generation only.

---

## 2. Glossary

| Term | Meaning |
|---|---|
| Page | A Notion page (including nested blocks). |
| Chunk | A contiguous text segment of a page, sized for embedding. |
| Sync | The process that pulls changes from Notion and publishes change events. |
| Retrieval | Finding the top-k chunks relevant to a query. |
| Grounded answer | An answer supported by retrieved chunks, with citations. |
| Domain event | An immutable message published by a service when something happened in its domain. |
| Contract | An OpenAPI document (sync APIs) or JSON Schema (events) that defines a service boundary. |

---

## 3. Architecture

### 3.1 Services

```
                     React SPA (S3 + CloudFront)
                                │ HTTPS (JSON + SSE)
                     ┌──────────▼───────────┐
                     │  platform            │  shared HTTP API, authorizer,
                     │                      │  EventBridge bus, alarms, budget
                     └───┬──────────┬───────┘
                         │          │
              ┌──────────▼──┐   ┌───▼─────────────┐
              │ chat        │──▶│ knowledge       │◀── events ──┐
              │ service     │ search API          │             │
              │ (DynamoDB)  │   │ (vector index,  │      ┌──────┴────────┐
              └──────┬──────┘   │  chunk metadata)│      │ ingestion     │
                     │          └─────────────────┘      │ service       │──▶ Notion API
                  OpenAI                                 │ (DynamoDB)    │
                  (LLM)                                  └───────────────┘
```

| Service | Responsibility | Owns (data) | Public API | Talks to |
|---|---|---|---|---|
| **ingestion** | Connect to Notion, detect changes, track sync runs, publish page events | `pages`, `sync_runs` (DynamoDB) | `POST /sync`, `GET /sync/runs` | Notion API; publishes events |
| **knowledge** | Chunk, embed and index page content; serve semantic search | `chunks` (DynamoDB) + vector index | none public; internal `POST /search` | Consumes events; embedding provider |
| **chat** | Conversations, prompt building, answer generation, citations, feedback | `conversations`, `messages`, `feedback` (DynamoDB) | `/chat/ask`, `/conversations`, `/messages/{id}/feedback` | Knowledge `/search`; LLM provider |
| **platform** | Shared edge and infra: HTTP API, authorizer, event bus, DLQs, alarms, budget | none | routing, auth | all |

The frontend is a client, not a service; it only calls the public APIs through the platform.

### 3.2 Why this split

The boundaries follow different scaling and failure profiles, not technical layers:
- **ingestion**: bursty, batch, rate-limited by Notion, tolerant of delay.
- **knowledge**: write path is throttled by embedding quotas; read path is latency-sensitive and read-heavy.
- **chat**: interactive, latency-sensitive, streaming, driven by user concurrency.

The system is deliberately kept to three domain services. Splitting further is not allowed without an ADR that names the scaling or ownership reason (see 12, item 10).

### 3.3 Principles

- P1. **Service autonomy**: each service is independently buildable, testable and deployable (`serverless deploy` per service). Deploying one service must not require redeploying another.
- P2. **Data ownership**: a service's tables and indexes are private. No service reads or writes another service's data store; IAM enforces this. Data crosses boundaries only through APIs or events.
- P3. **Contracts first**: every API and event has a contract in `/contracts` before implementation. Contracts are versioned and changes must be backward compatible within a major version.
- P4. **Async by default between services** when the caller does not need an immediate answer (ingestion to knowledge). Synchronous calls are used only where the user is waiting (chat to knowledge search), with a timeout and a defined degraded behaviour.
- P5. **Idempotency**: every event consumer and handler tolerates duplicates and reordering. Events carry an `event_id` and a page `version`; consumers ignore stale versions.
- P6. **Failure isolation**: a failure or slowness in one service must not take down others. Every cross-service call has timeout, retry with backoff and jitter, and a documented fallback. Failed async messages land in a DLQ with a documented replay procedure.
- P7. **Least-privilege IAM**: one role per function, scoped to exact resources.
- P8. **Infrastructure is code**: no resource is created or modified from the console.
- P9. **Observable by default**: a request id / trace id propagates through every synchronous call and event.
- P10. **Shared code is minimal**: services may share `/libs/common` (logging, tracing, config, HTTP client with retry) and generated contract types. They MUST NOT share domain logic or data models beyond contracts.

### 3.4 Lambda constraints the design must respect

- Max execution time is 15 minutes; ingestion must be resumable.
- Synchronous API responses are subject to API timeouts; the chat endpoint therefore uses response streaming (FR-19).
- No persistent local disk (only `/tmp`); no in-process cache assumed to survive.
- Cold starts affect p95; heavy imports are lazy and dependencies kept small.

### 3.5 Interactions

**Sync flow (async)**
1. Schedule or `POST /sync` starts an ingestion run.
2. Ingestion lists changed pages, stores page state and publishes `page.upserted` / `page.deleted` events to the bus.
3. Knowledge consumes events from its SQS queue, chunks, embeds and updates the index, and publishes `page.indexed` (or `page.index_failed`).
4. Ingestion consumes `page.indexed` / `page.index_failed` to update page status and sync run counters.

**Ask flow (sync)**
1. Frontend calls `POST /chat/ask` (through the platform, streaming).
2. Chat calls knowledge `POST /search` with the question.
3. Chat builds the prompt from the returned chunks, streams the LLM answer, persists the message and citations.

---

## 4. Tech stack and constraints

- Runtime: Python 3.12 on AWS Lambda (arm64).
- Lambda tooling: AWS Lambda Powertools for Python (logging, tracing, metrics, event handling, validation), Pydantic v2 for models.
- IaC: Serverless Framework, one `serverless.yml` per service plus one for `platform`. Non-function resources (DynamoDB, SQS, EventBridge, S3, CloudFront, alarms, budget) are declared in `resources` as CloudFormation. Cross-service references use exported CloudFormation outputs or SSM parameters, never hard-coded ARNs.
- Messaging: Amazon EventBridge (custom bus) for domain events; SQS (with DLQ) as the consumer buffer per subscribing service.
- Data: DynamoDB (on-demand), one table set per service. Vector index owned by knowledge (v1 default: S3 Vectors; alternatives evaluated in ADR-0002).
- AI: OpenAI as the v1 default, matching the PoC (gpt-4o-mini for generation, OpenAI embeddings for indexing), called through the provider SDK from the owning service (knowledge embeds, chat generates). Amazon Bedrock is the alternative evaluated in ADR-0006. Model ids and embedding dimensions are pinned in configuration, never taken from library defaults.
- Frontend: React 18 + TypeScript, Vite; S3 + CloudFront.
- Local dev: each service runs locally with in-memory fakes or `moto`/LocalStack; the PoC's Chroma may be used as a local vector index for knowledge.
- Tooling: `uv` or `pip-tools` for dependency locking per service, `ruff`, `mypy`, `pytest`, `cfn-lint`, `eslint`, `vitest`.
- Config: environment variables and SSM Parameter Store; secrets in Secrets Manager. No secrets in the repo.

"v1 default" choices are recorded as ADRs and can be revised without changing other services, because the choice is private to the owning service.

---

## 5. Repository layout (target)

```
/services
  /ingestion    src/, tests/, serverless.yml, openapi.yaml
  /knowledge    src/, tests/, serverless.yml, openapi.yaml
  /chat         src/, tests/, serverless.yml, openapi.yaml
/platform       serverless.yml (HTTP API, authorizer, bus, DLQs, alarms, budget)
/contracts
  /openapi      per-service API contracts
  /events       JSON Schemas for domain events
/libs/common    logging, tracing, config, resilient HTTP client (no domain code)
/frontend
/docs
  SPEC.md, ROADMAP.md, ADR/, traceability.md
/legacy_poc     original Gradio + Chroma code, read-only reference
```

Each service has its own dependency lock file and test suite. Cross-service imports are forbidden; a lint rule enforces that `services/a` never imports `services/b`.

---

## 6. Functional requirements

Each requirement is testable and has an owning service. IDs are stable identifiers, not a sequence: requirements added later appear at the end of their service group. Agents MUST add at least one automated test per requirement, named with the requirement ID, inside the owning service.

### 6.1 ingestion service

- **FR-1** Sync pulls pages from the configured Notion workspace/database using the Notion API.
- **FR-2** Sync is incremental: a page is reprocessed only if its `last_edited_time` is newer than the stored value.
- **FR-3** Pages deleted or archived in Notion result in a `page.deleted` event on the next sync.
- **FR-4** Sync is idempotent: running it twice with no Notion changes publishes no events.
- **FR-5** Each sync creates a `SyncRun` record with status, counts (created/updated/deleted/failed), start/end times and error summaries.
- **FR-6** A failure on one page does not abort the run; the page is recorded as failed and retried on the next run.
- **FR-7** Sync is resumable: near its deadline it persists a cursor and stops cleanly with status `partial`; the next invocation continues from the cursor.
- **FR-8** Sync is triggered by a schedule (EventBridge Scheduler) and on demand via `POST /sync`. Concurrent runs are prevented (run lock with expiry).
- **FR-9** Ingestion updates page status and run counters from `page.indexed` / `page.index_failed` events.
- **FR-29** The sync scope is a configured list of Notion root pages (configuration, not code). The PoC's four root pages (Projects, Areas, Resources, Archive) are the initial scope.
- **FR-30** Traversal treats every Notion child page as its own Page (own id, title, URL, `last_edited_time`, parent path and root section). Child page content is NOT flattened into its parent. Acceptance: given a root page with two child pages, then three pages are produced, and a citation for text in a child page links to that child page.
- **FR-31** Block-to-text conversion covers at least the PoC's block types plus tables (rows), bookmarks (title and URL) and child page titles. Unsupported block types are skipped and counted per type in the sync run metrics, never dropped silently.
- **FR-32** The Notion client checks HTTP status before parsing, honors rate limits (`429` and `Retry-After`), retries with backoff and jitter, and maps error payloads to structured errors; an error response never raises an unhandled exception.

**Acceptance (FR-2)**: given a page unchanged since the last sync, when sync runs, then no event is published for it.
**Acceptance (FR-7)**: given a workspace larger than one invocation can process, when the deadline is near, then the run ends `partial` with a stored cursor, and a subsequent run completes the remaining pages without republishing finished ones.

### 6.2 knowledge service

- **FR-10** Consumes `page.upserted`: converts the content to text preserving headings and chunks it (heading-aware; configurable). The baseline configuration matches the PoC (1000 characters, 200 overlap) so results are comparable; any change to the defaults must be justified by the evaluation in section 13.
- **FR-11** Each chunk stores page id, page title, heading path, position, content hash and Notion URL.
- **FR-12** Embeddings are generated only for chunks whose content hash changed.
- **FR-13** The embedding model id and dimension are stored with each vector; a mismatch with configuration is detected and reported, forcing a re-index (never silently mixing models).
- **FR-14** Consumes `page.deleted`: removes all chunks and vectors of the page.
- **FR-15** Ignores events older than the stored page version (out-of-order safe) and tolerates duplicates.
- **FR-16** `POST /search` (internal, IAM-authenticated) accepts a query, `k` (default 10, as in the PoC baseline; tuned through evaluation) and optional section filters, and returns chunks with scores and citation metadata, filtered by a configurable minimum similarity.
- **FR-17** Publishes `page.indexed` or `page.index_failed` after processing each page event.
- **FR-34** Every chunk carries `section` (the root section, e.g. Projects, Areas, Resources, Archive) and `path` metadata. `/search` supports `sections` and `exclude_sections` filters; the default behavior (for example whether Archive is searched) is configuration (see OQ-4).
- **FR-35** Upserting a page replaces its chunks: chunks whose position no longer exists or whose content changed are deleted, so the index never retains outdated content for that page.
- **FR-36** The similarity metric (cosine) is explicit in configuration and stored with the index; the minimum-similarity threshold is defined against that metric and re-calibrated whenever the embedding model changes.

**Acceptance (FR-15)**: given `page.upserted` v3 already indexed, when v2 arrives afterwards, then the index is unchanged.

### 6.3 chat service

- **FR-18** `POST /chat/ask` accepts a question and optional conversation id.
- **FR-19** The answer is streamed via Server-Sent Events (Lambda response streaming): events `token`, `citations`, `done`, `error`.
- **FR-20** If knowledge returns no chunk above the threshold, the assistant MUST answer that it did not find relevant information in the notes and MUST NOT answer from general model knowledge.
- **FR-21** Every answer includes citations: page title, Notion URL and chunk ids used.
- **FR-22** The prompt instructs the model to use only the provided context; the template is versioned (`prompt_version` stored per message). Generation temperature defaults to 0.2 or lower and is configurable (the PoC used 0.7).
- **FR-23** Conversations and messages are persisted with per-stage latencies (search, first token, total).
- **FR-24** If knowledge is unavailable or times out, chat returns a clear error event and persists the failed turn; it never answers ungrounded.
- **FR-25** The user can rate an answer (up/down, optional comment) and list or delete conversations.
- **FR-37** Follow-up questions are rewritten into a standalone query using the last N turns (default 6) before calling `/search`; the rewritten query is stored with the message for debugging.
- **FR-38** Chat functions are stateless: conversation history is loaded from and saved to the chat service's store on every request, and truncated to a configured turn or token budget. No in-process global memory.

**Acceptance (FR-20)**: given a question unrelated to any note content, then the response states no relevant notes were found and contains zero citations.
**Acceptance (FR-24)**: given knowledge times out, then the stream ends with an `error` event and no `token` events.

### 6.4 frontend

- **FR-26** Chat view with streaming answer rendering, citations as links, and a visible "no relevant notes" state.
- **FR-27** Sync status view: last run, counts, failures, and a button to trigger a sync.
- **FR-28** Conversation history list with delete.

---

## 7. Contracts

Contracts live in `/contracts` and are the authoritative source; services and the frontend generate types from them. CI fails if an implementation diverges from its contract.

### 7.1 Public API (through platform)

Base path `/api`. JSON, UTF-8. Errors follow RFC 7807 (`application/problem+json`).

| Method | Path | Owner | Description |
|---|---|---|---|
| POST | `/chat/ask` | chat | Ask a question; SSE stream. |
| GET | `/conversations` | chat | List conversations (cursor pagination). |
| GET | `/conversations/{id}` | chat | Messages and citations. |
| DELETE | `/conversations/{id}` | chat | Delete a conversation. |
| POST | `/messages/{id}/feedback` | chat | Rate an answer. |
| POST | `/sync` | ingestion | Start a sync; `202` with run id. |
| GET | `/sync/runs` | ingestion | List runs. |
| GET | `/sync/runs/{id}` | ingestion | Run detail. |
| GET | `/health` | platform | Aggregated readiness of services. |

Rules: cursor pagination (`limit` max 100); `X-Request-Id` on every response, propagated as trace id; CORS limited to the CloudFront origin; auth v1 is a static API token checked by the platform Lambda authorizer (Secrets Manager), replaceable by Cognito without changing shapes.

### 7.2 Internal API

| Method | Path | Owner | Consumer | Description |
|---|---|---|---|---|
| POST | `/internal/search` | knowledge | chat | Semantic search. IAM-authenticated, not exposed publicly. |

### 7.3 Domain events (EventBridge, source per service)

| Event | Producer | Consumers | Key fields |
|---|---|---|---|
| `page.upserted` | ingestion | knowledge | `event_id`, `page_id`, `version`, `title`, `url`, `content` (or content reference), `occurred_at` |
| `page.deleted` | ingestion | knowledge | `event_id`, `page_id`, `version`, `occurred_at` |
| `page.indexed` | knowledge | ingestion | `event_id`, `page_id`, `version`, `chunk_count`, `embedding_model` |
| `page.index_failed` | knowledge | ingestion | `event_id`, `page_id`, `version`, `reason` |

Event rules: envelope with `event_id`, `type`, `schema_version`, `trace_id`; additive changes only within a major version; large content is stored in S3 and referenced (EventBridge and SQS payload limits), decided in ADR-0003.

---

## 8. Data ownership

Each service documents its DynamoDB access patterns in `docs/ADR/` and derives keys from them.

- **ingestion**: get page by Notion id; list pages changed since a timestamp; get/list sync runs (latest first); get the run lock.
- **knowledge**: list chunks of a page; get chunk by id; vector index queried by similarity. The vector index is a derived store, fully rebuildable by replaying page events or re-running a sync.
- **chat**: list conversations (latest first); messages of a conversation in order; citations and feedback per message.

No cross-service table access. If chat needs page titles or URLs, it reads them from the search response (citation metadata), never from ingestion's tables.

---

## 9. Non-functional requirements

- **NFR-1 Latency**: time to first token p95 < 3 s warm on the reference dataset (`docs/benchmarks.md`); cold-start impact reported separately. Latency budget per stage is documented (search, LLM first token).
- **NFR-2 Index freshness**: p95 lag from Notion edit to searchable < 15 minutes with a 10-minute schedule (measured via events).
- **NFR-3 Reliability**: a Notion or AI-provider outage produces clear errors and never corrupts data. All async consumers have DLQs and a documented replay procedure. Sync calls are protected by timeouts and retries.
- **NFR-4 Observability**: structured JSON logs, X-Ray traces across services, custom metrics per stage, alarms on error rate, DLQ depth and throttles.
- **NFR-5 Security**: least-privilege IAM per function; services cannot access each other's data stores; secrets in Secrets Manager; read-only Notion token; secrets and tokens are never printed or logged; encryption at rest.
- **NFR-6 Privacy**: note content is sent only to configured providers; documented in the README.
- **NFR-7 Reproducibility**: a clean clone deploys with a documented script that runs `serverless deploy` per service in dependency order (platform, then services); local runs work with fakes.
- **NFR-8 Cost**: idle cost near zero; monthly estimate documented; budget alarm provisioned by the platform stack.
- **NFR-9 Independent deployability**: each service can be deployed alone in CI without breaking the others (verified by contract tests).

---

## 10. Migration from the PoC

The Gradio + Chroma + LangChain PoC (`vectorize.py`, `run_chat.py`) lives in `/legacy_poc` as a read-only reference.

### 10.1 What the PoC does today

- **Ingestion**: reads four fixed root pages of a second-brain style Notion workspace, fetches all descendant blocks recursively, and concatenates them into one text per root page.
- **Indexing**: recursive character splitter (1000 characters, 200 overlap); OpenAI embeddings using the library's default model; Chroma persisted locally; deterministic chunk ids `{page_id}-chunk-{i}`.
- **Chat**: LangChain `ConversationalRetrievalChain` (question rewriting plus retrieval, k=10), gpt-4o-mini at temperature 0.7, one global in-memory conversation buffer, Gradio UI.

### 10.2 Findings and how this spec responds

| # | Finding in the PoC | Consequence | Spec response |
|---|---|---|---|
| 1 | Child pages appear to be flattened into their root page, and chunk metadata carries the root's title and URL | Citations would point to a section, not the note; page-level incremental sync is impossible | FR-2, FR-30 |
| 2 | Every run re-embeds everything; re-adding existing ids may be skipped rather than updated (depends on the Chroma version); chunks of shrunken or deleted pages are never removed | Stale content, wasted cost | FR-2, FR-12, FR-14, FR-35 |
| 3 | Notion responses are parsed without checking status; no retries or rate-limit handling; sequential recursion | A `429` or error payload crashes the run | FR-6, FR-32 |
| 4 | Unsupported block types (tables, bookmarks, child page titles and others) return empty text | Silent information loss | FR-31 |
| 5 | Splitting is character-based and ignores the headings the converter emits | Chunks can straddle topics | FR-10 (baseline kept for comparison) |
| 6 | No similarity threshold and no source documents returned | Cannot answer "not found"; no citations | FR-16, FR-20, FR-21 |
| 7 | Temperature 0.7 for grounded Q&A | More variation and hallucination risk | FR-22 |
| 8 | One global conversation buffer in process memory | Not stateless; incompatible with Lambda; unbounded growth | FR-38 |
| 9 | Follow-up rewriting happens implicitly inside the chain | Would be lost when the chain is dropped | FR-37 |
| 10 | Embedding model and distance metric are library defaults | Silent change on upgrade; threshold semantics unclear | FR-13, FR-36, OQ-12 |
| 11 | The Notion token is printed to stdout; page ids are hardcoded | Secret leakage; configuration in code | NFR-5, FR-29 |
| 12 | Archive is indexed with active content and no section metadata | Stale material competes with current notes | FR-34, OQ-4 |

### 10.3 Keep, change, drop

- **Keep**: recursive block traversal and cursor pagination; markdown-style heading conversion; deterministic chunk ids by page and position (plus content hash); the PoC's chunking parameters as the baseline configuration; the source/title/page-id metadata idea.
- **Change**: everything in the table above.
- **Drop**: Gradio (replaced by the React frontend) and, as a proposal, LangChain in deployed services (ADR-0007). Rationale: import weight and package size hurt Lambda cold starts (NFR-1); the legacy chain and memory classes are on LangChain's deprecation path; and the flow (embed, search, prompt, stream) is small enough to implement directly with the provider SDK. LangChain may still be used in local experiments. Chroma remains only as a local vector index for knowledge.

### 10.4 Migration rules

1. Do not import Gradio anywhere in the new code. Do not import LangChain in deployed code unless ADR-0007 is rejected.
2. Existing Chroma data is not migrated; the index is rebuilt by a sync. Differences (chunk size, embedding model) are recorded in an ADR.
3. Run the PoC on the evaluation questions first and record its hit-rate as the baseline (section 13).
4. Remove `/legacy_poc` only when FR-18 to FR-21 pass end to end on the new stack and the baseline is met.

---

## 11. Deployment and environments

- Environments: `dev` (developer account or stage) and `prod`; stage names are Serverless stages.
- Deploy order: platform first, then ingestion, knowledge and chat (any order among the three once the platform exists).
- Each service's CI pipeline runs its unit tests, contract tests and `cfn-lint`, then deploys only that service.
- Rollback: redeploy the previous version of the affected service; event and API contracts guarantee compatibility within a major version.

---

## 12. Scalability and bottleneck roadmap

Documented in `docs/ROADMAP.md`. Each item states trigger metric, mitigation and the seam present in v1.

| # | Bottleneck | Trigger | Mitigation | v1 seam |
|---|---|---|---|---|
| 1 | Ingestion exceeds one Lambda run (15 min) | Runs end `partial` repeatedly | Fan out per page via SQS to a worker Lambda; Step Functions if orchestration visibility is needed | Resumable cursor (FR-7); page-level processing unit |
| 2 | Notion API rate limits | HTTP 429 | Token-bucket client; reserved concurrency on workers | Resilient HTTP client in `libs/common` |
| 3 | Embedding throughput and provider quotas | Throttling in knowledge consumers | Cap consumer concurrency, batching, backoff, provider fallback | SQS buffer + reserved concurrency |
| 4 | Event backlog / freshness | Freshness lag above NFR-2, growing queue depth | Scale consumers, prioritise deletes and recent edits, partition queues | Per-service queues and DLQ alarms |
| 5 | Search latency and vector index limits | p95 search above budget; recall drops | Cache query embeddings and results; move to OpenSearch Serverless, Aurora pgvector or Qdrant | Index private to knowledge (swap without touching chat) |
| 6 | Chat concurrency and cold starts | p95 TTFT above NFR-1 | Provisioned concurrency for the ask function, smaller packages, answer cache | Thin handlers; init-time metrics |
| 7 | Synchronous chat-to-knowledge chattiness | Search dominates latency or failure rate | Tighter timeouts and retries, circuit breaker, co-locate or cache hot queries | Timeout and fallback defined (FR-24) |
| 8 | Eventual consistency confusion | Users query right after edits | Show index freshness in the UI using `page.indexed` data | Events carry version and timestamps |
| 9 | Schema and contract evolution | Breaking change needed | Versioned events and APIs, dual-publish period, consumer-driven contract tests | `schema_version` on every event |
| 10 | Over-fragmentation | Ownership or scaling need for a new split | Requires an ADR naming the reason; default is to keep three services | Boundaries documented in 3.2 |
| 11 | DynamoDB hot partitions / item size | Throttled writes; large text | Key redesign with write sharding; chunk text to S3 | Access patterns documented per service |
| 12 | Multi-user / multi-tenant | More than one workspace | Tenant id in keys, events and vector metadata; Cognito; per-tenant quotas | Authorizer and event envelope carry identity fields |
| 13 | Distributed debugging | Incidents spanning services | Trace and request-id propagation, log correlation, dashboards per flow | P9 |

Each adopted mitigation requires an ADR in `docs/ADR/`.

---

## 13. Validation strategy

- **Unit**: per service, with in-memory fakes for AWS and external calls; chunking, deadline handling, version ordering and prompt building have edge-case tests.
- **Contract**: OpenAPI and JSON Schema validation in CI; producer and consumer tests for every event and the search API; generated types for the frontend.
- **Integration (per service)**: handlers against `moto` or LocalStack; Notion and AI providers stubbed.
- **End-to-end**: a smoke suite in `dev` that runs a sync on a fixture workspace, waits for `page.indexed`, then asks a question and verifies citations.
- **Infrastructure**: `cfn-lint` on generated templates plus IAM assertions (no wildcards; no cross-service data access).
- **RAG evaluation**: fixed question/expected-source pairs in `services/chat/tests/eval/`; report hit-rate@k and groundedness; regression below the documented threshold fails CI. The PoC configuration (1000/200 chunks, k=10, gpt-4o-mini) is recorded as the baseline, and the new system must meet or beat it on the same question set.
- **Resilience**: tests for duplicate, out-of-order and poison events; timeout and degraded-mode tests for chat to knowledge.
- **Traceability**: `docs/traceability.md` maps each FR/NFR to tests; CI fails if a requirement has no test.

---

## 14. Rules for AI agents working in this repo

1. Read this spec and `docs/ADR/` before making changes. Cite requirement IDs in commit messages and PR descriptions.
2. One service per PR. If a change needs two services, split it: contract first, then producer, then consumer.
3. Contract changes come first, in their own PR, and must be backward compatible within a major version.
4. Never access another service's data store or import another service's code. Cross-service interaction goes through contracts only.
5. Never change behavior described in this spec silently. If the spec is wrong or incomplete, propose an amendment to `SPEC.md` first, in a separate commit.
6. Write or update tests before or with the implementation. A change without tests for its requirement is not done.
7. Do not add services, dependencies, AWS resources or providers not listed here without an ADR.
8. Do not call real external services in tests. Do not commit secrets or real Notion content. Never print or log secrets or tokens.
9. Every handler and consumer must be idempotent and have a documented timeout, retry and failure path (DLQ or error response).
10. Never widen an IAM policy to make something work; propose the minimal permission and justify it in the PR.
11. When uncertain, list the assumption explicitly in the PR description rather than guessing silently.

**Definition of done**
- Requirement and contract tests pass; `ruff`, `mypy`, `eslint`, type checks and `cfn-lint` are clean.
- Contracts, traceability docs and ADRs are updated.
- The affected service deploys independently in `dev`, and the end-to-end smoke test passes.

---

## 15. Open questions

- OQ-1. AWS region? (Bedrock model availability and data residency vary by region.)
- OQ-2. The PoC uses OpenAI (gpt-4o-mini and OpenAI embeddings). Keep OpenAI as the v1 default (parity with the baseline, but note content leaves AWS; see NFR-6), or move to Bedrock? Decided in ADR-0006.
- OQ-3. Streaming transport for chat: Lambda Function URL with response streaming, or API Gateway with response streaming? Confirm current support and limits before ADR-0004.
- OQ-4. Scope refinements beyond the four PoC root pages: are Notion databases (rows) under those roots in scope, and should Archive be searched by default or only on request?
- OQ-5. Attachments and images in scope, or text blocks only? (Default: text only.)
- OQ-6. Language(s) of the notes? (Affects embedding model and prompt language.)
- OQ-7. Public demo planned? (Affects auth, cost alarms and rate limiting.)
- OQ-8. Serverless Framework licensing: confirm current terms for your use and pin the major version in an ADR (ADR-0005).
- OQ-9. Confirm how the chosen Serverless Framework version configures Lambda response streaming before ADR-0004.
- OQ-10. Event payload strategy: content inline vs. S3 reference (size limits); decided in ADR-0003.
- OQ-11. Proposed: no LangChain in deployed services (ADR-0007). Confirm, or keep it and accept the cold-start and package-size cost.
- OQ-12. Should the embedding model change from the PoC's library default? If so, the index is rebuilt and the threshold re-calibrated (FR-13, FR-36).
