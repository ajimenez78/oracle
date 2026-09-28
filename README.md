# Oracle

A personal oracle built on your own second brain: ask questions in natural language and get answers based only on your Notion workspace, with links to the pages the answers came from.

## Status

Early stage. The design is in [`specs/SPEC.md`](specs/SPEC.md), which is the source of truth for the project. The code in [`legacy/`](legacy/) is the original proof of concept, kept only as a reference.

## How it will work

Oracle is a retrieval-augmented generation (RAG) system built as serverless microservices on AWS:

| Component | What it does |
|---|---|
| **ingestion** | Syncs pages from Notion on a schedule or on demand. Only changed pages are processed. |
| **knowledge** | Splits pages into chunks, creates embeddings, and serves semantic search. |
| **chat** | Answers questions from the retrieved notes only, streams the answer and cites its sources. If no relevant notes are found, it says so instead of guessing. |
| **platform** | Shared HTTP API, authentication, event bus, alarms and budget. |
| **frontend** | React web app for chatting, browsing conversations and checking sync status. |

Services talk to each other through versioned contracts (OpenAPI and event schemas) and can be deployed independently.

**Stack:** Python 3.12 on AWS Lambda, Serverless Framework, EventBridge + SQS, DynamoDB, S3 Vectors, OpenAI (gpt-4o-mini and OpenAI embeddings), React + TypeScript.

## Privacy

Your note content is sent only to the configured AI provider (OpenAI by default) to create embeddings and generate answers. The Notion integration only needs read access.

## Legacy proof of concept

`legacy/` contains the first prototype: `vectorize.py` indexes four Notion root pages into a local Chroma database, and `run_chat.py` starts a Gradio chat over it using LangChain. It is kept for reference and as the quality baseline the new system must meet or beat. It is not part of the new architecture.

## License

[MIT](LICENSE)
