# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Oracle: a personal assistant that answers questions using only the owner's Notion "second brain" and cites the pages it used (RAG). It is also meant as a reference implementation of a serverless microservices system on AWS.

**`specs/SPEC.md` is the source of truth.** If code and spec disagree, the spec wins. Read it (and `docs/ADR/` once it exists) before making changes. Its section 14 has binding rules for AI agents; the most important are summarized below.

## Current state

- Nothing from the target architecture is built yet. There are no build, lint or test commands so far.
- `legacy/` holds the original PoC (the spec calls this folder `/legacy_poc`). Treat it as a read-only reference and never import from it:
  - `legacy/vectorize.py`: fetches four hardcoded Notion root pages (Projects, Areas, Resources, Archive), flattens every descendant block into one text per root, splits it with LangChain's `RecursiveCharacterTextSplitter` (1000/200) and stores OpenAI embeddings in a local Chroma DB (`personal_vector_db`, collection `notion_notes`).
  - `legacy/run_chat.py`: Gradio chat over a LangChain `ConversationalRetrievalChain` (gpt-4o-mini, temperature 0.7, k=10, one global in-memory buffer).
  - Spec section 10 lists the PoC's defects and says what to keep, change and drop. Its configuration (1000/200 chunks, k=10, gpt-4o-mini) is the **RAG evaluation baseline** that the new system must meet or beat.
- The spec says the layout will be `/docs/SPEC.md`, but the spec currently lives in `specs/`.

## Target architecture (spec sections 3–5)

There are three domain services plus a platform stack. Each one is deployed on its own with `serverless deploy`:

- **ingestion**: Notion API → per-page state and sync runs (DynamoDB). Publishes `page.upserted` / `page.deleted`. Incremental (`last_edited_time`), resumable near the 15-minute Lambda deadline via a cursor, with a run lock. Every Notion child page becomes its own Page; content is never flattened into the parent.
- **knowledge**: consumes page events from SQS, chunks by heading and embeds only chunks whose content hash changed. Stores chunks in DynamoDB and vectors in S3 Vectors (v1 default). Serves the internal IAM-authenticated `POST /internal/search` and publishes `page.indexed` / `page.index_failed`.
- **chat**: `POST /chat/ask` streams SSE (`token`, `citations`, `done`, `error`). Rewrites follow-up questions into a standalone query, calls knowledge search, then answers **only** from the returned chunks, with citations. If nothing clears the similarity threshold, or search fails, it must say so and must not answer from general knowledge. Stateless: conversation history lives in DynamoDB.
- **platform**: HTTP API, Lambda authorizer (static token), EventBridge bus, DLQs, alarms and budget. Deploy it first.
- **frontend**: React 18 + TypeScript + Vite on S3/CloudFront. It is a client only.

Target layout: `services/{ingestion,knowledge,chat}` (each with its own `src/`, `tests/`, `serverless.yml`, `openapi.yaml` and lock file), `platform/`, `contracts/{openapi,events}`, `libs/common`, `frontend/`, `docs/` (ROADMAP, ADR/, traceability.md).

Stack: Python 3.12 on arm64 Lambda, AWS Lambda Powertools, Pydantic v2, Serverless Framework, EventBridge + SQS, DynamoDB on-demand, OpenAI (gpt-4o-mini; model IDs and embedding dimensions pinned in config). Tooling: `uv` or pip-tools, `ruff`, `mypy`, `pytest`, `moto`/LocalStack, `cfn-lint`, `eslint`, `vitest`.

## Rules that shape every change

- **Service boundaries:** a service never imports another service's code and never touches another service's data store. Services interact only through contracts in `/contracts`. `libs/common` holds only logging, tracing, config and the resilient HTTP client, never domain logic.
- **Contracts first:** a contract change goes in its own PR and must be backward compatible within a major version. A change that spans services is split: contract, then producer, then consumer. Only one service per PR.
- **Every event consumer is idempotent and safe with out-of-order events:** events carry `event_id` and a page `version`, and stale versions are ignored. Every cross-service call has a timeout, retry with backoff and jitter, and a documented fallback or DLQ.
- **Requirement IDs:** each FR must have at least one automated test in the owning service, named with its ID (e.g. `test_fr15_...`). Cite FR/NFR IDs in commit messages and PR descriptions. `docs/traceability.md` maps requirements to tests.
- **No LangChain in deployed code** (proposed in ADR-0007) and no Gradio anywhere. Call the provider SDKs directly.
- **ADR required** before adding any service, dependency, AWS resource or provider not in the spec. Never widen IAM policies to make something work.
- **No silent spec changes:** if the spec is wrong, propose an amendment to `SPEC.md` in a separate commit first.
- **No real external calls in tests.** Never commit or log secrets or real Notion content. (The PoC prints the Notion token; don't copy that.)
- Open questions (region, streaming transport, Archive search default, embedding model, etc.) are listed in spec section 15. Don't settle them silently; state any assumption in the PR.

## Git workflow

- Day-to-day work happens on `develop`; `main` is the target branch for PRs.
