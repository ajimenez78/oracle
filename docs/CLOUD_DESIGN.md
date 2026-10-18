# Cloud design: serverless deployment of the PoC

> Status: Proposal · Scope: interim deployment of the current PoC (`src/oracle/vectorize.py`, `src/oracle/run_chat.py`)
> This is **not** the target architecture. [`SPEC.md`](SPEC.md) remains the source of truth. This document describes the smallest change that runs the PoC on AWS at close to zero cost while the target system is built. Section 10 lists where it departs from the spec.

---

## 1. Goals

- Expose the two PoC functions as REST endpoints: **vectorize** (index Notion) and **chat** (answer a question).
- Run them on AWS Lambda with no servers to manage.
- Keep AWS cost close to $0 with the always-free allowances. The only meaningful cost is the model provider (OpenAI by default).
- Reuse the existing code with as few changes as possible.

**Non-goals:** the fixes listed in SPEC section 10.2 (incremental sync, per-page citations, similarity threshold, streaming, persisted conversations). The target system handles those.

---

## 2. Architecture

```
  Local Gradio UI / curl / any client
        │  HTTPS + X-Api-Key header
        │
        ├──────────────────────────────┐
        ▼                              ▼
 ┌───────────────────┐        ┌────────────────────┐      EventBridge Scheduler
 │ Lambda: chat      │        │ Lambda: vectorize  │◀──── (e.g. daily)
 │ Function URL      │        │ Function URL       │
 │ POST /            │        │ POST /             │──────▶ Notion API
 └───┬──────────┬────┘        └───┬────────────┬───┘
     │ query    │ generate        │ embed      │ put/delete
     ▼          ▼                 ▼            ▼
 ┌───────────────────┐    ┌──────────────┐  ┌───────────────────┐
 │ S3 Vectors        │    │ OpenAI       │  │ S3 Vectors        │
 │ bucket: oracle-   │◀───│ (embeddings, │  │ (same index)      │
 │ vectors           │    │  gpt-4o-mini)│  └───────────────────┘
 │ index: notion-    │    └──────────────┘
 │ notes             │
 └───────────────────┘
        SSM Parameter Store (SecureString): OpenAI key, Notion token, API key
```

| Component | AWS service | Notes |
|---|---|---|
| Chat endpoint | Lambda + Function URL | Stateless. The client sends the history with every request. |
| Vectorize endpoint | Lambda + Function URL | Also triggered on a schedule. Max 15 minutes per run. |
| Vector store | Amazon S3 Vectors | Replaces the local Chroma DB, shared by both functions. |
| Schedule | EventBridge Scheduler | Runs vectorize periodically. |
| Secrets | SSM Parameter Store (SecureString) | Free in the standard tier. |
| Logs | CloudWatch Logs | Set a short retention (e.g. 14 days). |

### 2.1 Why these choices

- **Function URLs instead of API Gateway.** They have no extra charge and allow the full 15-minute Lambda timeout. API Gateway cuts synchronous requests off at about 29 seconds, which is too short for vectorize.
- **S3 Vectors instead of Chroma.** Lambda has no persistent disk (only `/tmp`, which is erased), so a local Chroma DB written by vectorize would never be visible to chat. S3 Vectors is pay-per-use with no minimum charge, and `langchain-aws` ships an `AmazonS3Vectors` vector store, so the retriever code barely changes. Dropping `chromadb` also removes its heavy dependencies from the package.
- **SSM instead of Secrets Manager.** Secrets Manager charges per secret per month. SSM standard SecureString parameters are free.

---

## 3. API

Both endpoints require the header `X-Api-Key: <token>`. A request with a missing or wrong key gets `401`. Bodies are JSON in UTF-8.

### 3.1 Chat: `POST <chat-function-url>/`

Request:
```json
{
  "question": "What did I decide about the garden project?",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}
```

Response `200`:
```json
{ "answer": "..." }
```

Errors: `400` for invalid input (missing `question`, malformed `history`), `401` for auth, `502` if the model provider fails. The handler truncates `history` to the last N turns (default 6) to bound prompt size.

### 3.2 Vectorize: `POST <vectorize-function-url>/`

Request: empty body, or `{"page_ids": ["..."]}` to override the default root pages.

Response `200` (synchronous, returned when the run finishes):
```json
{
  "pages_processed": 4,
  "chunks_indexed": 512,
  "skipped": [{"kind": "block", "id": "...", "status": 404}],
  "duration_seconds": 183
}
```

The scheduled trigger calls the same handler with an empty event.

---

## 4. Data: S3 Vectors

- **Vector bucket:** `oracle-vectors` (created once by the deploy).
- **Index:** `notion-notes`, cosine distance. The dimension must match the embedding model.
- **Vector key:** `{page_id}-chunk-{i}`, the same deterministic IDs the PoC already uses.
- **Metadata per vector:** `source` (Notion URL), `title`, `page_id`, plus the chunk text, which `AmazonS3Vectors` stores by default.
- **Embedding model:** pin it explicitly in configuration (for example `text-embedding-3-small`, 1536 dimensions) instead of relying on the library default, so a library upgrade can never silently mix models.

### 4.1 Rebuild strategy

The PoC re-indexes everything on each run, and stale chunks from shrunken pages are never removed. With a dataset this small, the simplest correct approach is a **full rebuild** on each run:

1. List all vector keys in the index and delete them.
2. Re-crawl Notion and insert the new chunks.

During the rebuild (a few minutes), chat may return incomplete results. That's acceptable for personal use. If it becomes a problem, alternate between two indexes (`notion-notes-a` / `-b`) and keep the active name in an SSM parameter that chat reads at cold start.

---

## 5. Code changes

| File | Change |
|---|---|
| `src/oracle/vectorize.py` | Replace `Chroma(...)` with `AmazonS3Vectors(vector_bucket_name=..., index_name=..., embedding=...)`. Add the delete-then-insert rebuild (4.1). Return a summary dict instead of printing. |
| `src/oracle/run_chat.py` | Split into a module that builds the chain (vector store, retriever, LLM) at import time, so it's reused across warm invocations, and a function `answer(question, history) -> str`. Move the Gradio launch out of this module. |
| `src/oracle/handlers.py` (new) | `chat_handler(event, context)` and `vectorize_handler(event, context)`: parse the Function URL event, check `X-Api-Key`, call the logic above, and return JSON with status codes. |
| `src/oracle/config.py` (new) | Read configuration from environment variables: bucket, index, model ids, `k`, history limit, and secret parameter names. |
| `src/oracle/ui.py` (new, local only) | Gradio UI that calls the chat endpoint over HTTP. Never deployed. |
| `pyproject.toml` | Add `langchain-aws`. Remove `langchain-chroma`. Move `gradio` to an optional `ui` dependency group so it stays out of the Lambda package. |

Secrets are read once per cold start from SSM (`boto3` `get_parameter(WithDecryption=True)`) and never logged.

---

## 6. Infrastructure

Defined as code with the **Serverless Framework** (`serverless.yml` at the repo root), the same tool SPEC.md uses.

| Setting | chat | vectorize |
|---|---|---|
| Runtime / arch | Python 3.12 / arm64 | Python 3.12 / arm64 |
| Memory | 1024 MB (faster cold starts) | 512 MB |
| Timeout | 60 s | 900 s (15 min) |
| Function URL auth | `NONE` + `X-Api-Key` check | `NONE` + `X-Api-Key` check |
| Reserved concurrency | 2 (caps runaway cost) | 1 (no overlapping runs) |
| Trigger | Function URL | Function URL + EventBridge schedule |

**IAM (one role per function, least privilege):**
- chat: `s3vectors:QueryVectors` and `s3vectors:GetVectors` on the index, plus `ssm:GetParameter` on its parameters.
- vectorize: `s3vectors:PutVectors`, `ListVectors`, `DeleteVectors`, `GetIndex` and `CreateIndex` on the bucket and index, plus `ssm:GetParameter`.
- Verify the exact S3 Vectors action names against the current AWS docs before deploying.

**Packaging:** try a zip package first. Without `chromadb` it should fit Lambda's 250 MB unzipped limit. If it doesn't, switch to a container image in ECR (10 GB limit, a few cents a month of storage).

**Region:** choose one where S3 Vectors is available, ideally close to you (for example `eu-west-1` or `eu-south-2`). This is still open in SPEC OQ-1.

**Guardrails:** an AWS Budget alarm at a low threshold (e.g. $5/month) and an OpenAI usage limit on the API key.

---

## 7. Security

- **Authentication:** a random API key stored in SSM and checked in the handler with a constant-time comparison. Function URLs are public, so without this check anyone who found the URL could read your notes and spend your OpenAI credits. `AWS_IAM` auth is stronger, but browsers and Gradio can't sign requests easily, so it's left as an upgrade.
- **Secrets:** OpenAI key, Notion token and API key live only in SSM SecureString parameters. They're never written to environment files in the repo, and never printed or logged. Note that the current PoC prints the Notion token; remove that.
- **Notion token:** read-only integration.
- **Privacy:** note content is sent to the model provider (OpenAI) for embeddings and answers, as it is today.
- **CORS:** if a browser UI is added later, restrict it to that origin.

---

## 8. Cost estimate

Assumes personal use: about 1,000 questions per month and one vectorize run per day.

| Item | Monthly usage | Cost |
|---|---|---|
| Lambda requests and compute | ~1,030 requests, ~10,000 GB-s | $0 (always free: 1M requests, 400,000 GB-s) |
| Function URLs | | $0 |
| EventBridge Scheduler | ~30 invocations | $0 (free tier) |
| S3 Vectors storage | ~10–20 MB | < $0.01 |
| S3 Vectors queries and writes | ~1,000 queries, daily rebuild | < $0.05 |
| SSM Parameter Store (standard) | 3 parameters | $0 |
| CloudWatch Logs | small, 14-day retention | ~$0 (within free tier) |
| **AWS total** | | **≈ $0–0.10** |
| OpenAI (gpt-4o-mini + embeddings) | depends on usage | a few dollars at most |

S3 Vectors prices come from third-party sources (about $0.06/GB-month storage and $2.50 per million queries). Check the [S3 pricing page](https://aws.amazon.com/s3/pricing/) before relying on them. The daily full rebuild re-embeds every chunk. If OpenAI embedding cost matters, run vectorize weekly or on demand.

**Cheaper or free model options:** replace OpenAI with Ollama Cloud's free tier (chat only) or an OpenAI-compatible open-model API by changing the `ChatOpenAI` `base_url`. Embeddings would still need a provider. If the embedding model changes, the index must be rebuilt.

---

## 9. Limitations and risks

- **Vectorize must finish in 15 minutes.** The crawl is sequential. If the workspace grows past that, the run fails. The fix is the resumable or fan-out design in SPEC section 12, item 1.
- **Cold starts** of several seconds because of the LangChain imports. That's fine for personal use.
- **No streaming:** the chat answer arrives all at once.
- **Inherited PoC defects:** child pages flattened into root pages, so citations point to the root section; no similarity threshold, so it never says "not found"; temperature 0.7. See SPEC section 10.2.
- **Deprecated chain:** `ConversationalRetrievalChain` comes from `langchain-classic` and is on LangChain's deprecation path.
- **Rebuild window:** chat sees a partial index during vectorize (4.1).

---

## 10. Relation to SPEC.md

This design is a stepping stone. It deliberately departs from the spec in these ways:

| SPEC.md | This design | Why |
|---|---|---|
| Three services + platform stack, EventBridge + SQS | Two Lambdas, no events | Minimal change to the PoC |
| No LangChain in deployed code (ADR-0007, proposed) | LangChain deployed | Reuse the PoC unchanged |
| Platform HTTP API + Lambda authorizer | Function URLs + API key check in the handler | Free, no 29 s limit |
| Secrets Manager | SSM SecureString | Free |
| Conversations in DynamoDB (FR-38) | History sent by the client | Stateless with no extra resources |
| SSE streaming (FR-19) | Single JSON response | Simpler |
| Incremental, per-page sync | Full rebuild per run | Small dataset |

Things that carry over directly to the target system: S3 Vectors as the vector index (the spec's v1 default), Lambda arm64 with Python 3.12, the Serverless Framework, the SSM/IAM setup, and the budget alarm. This deployment also gives a running baseline for the RAG evaluation in SPEC section 13.

If this design is adopted as more than a temporary step, record it in an ADR and amend SPEC.md, as section 14 requires.
