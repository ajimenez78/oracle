## Context

`run_chat.py` wires `ConversationalRetrievalChain.from_llm(llm, retriever, memory)` and exposes it through `gr.ChatInterface(chat)`. Gradio already calls `chat(question, history)` with the session's prior messages, but the function ignores `history` and relies on the module-level `ConversationBufferMemory`. The chain (from `langchain_classic`) also accepts history directly as a `chat_history` input. See proposal.md for motivation.

Note: `openspec/config.yaml` currently describes the stack as "Python, Django, aws"; that is inaccurate (the spec targets Lambda + Serverless Framework, no Django) and was ignored here. Fixing it is out of scope for this change.

## Goals / Non-Goals

**Goals:**
- Feed the chain the history Gradio provides, per call.
- Keep the chain, prompts and retrieval settings byte-for-byte unchanged.

**Non-Goals:**
- Removing the `ConversationalRetrievalChain` deprecation (may surface once the memory warning is gone).
- Any automated test harness for the PoC.

## Decisions

**Pass `chat_history` per call instead of using a memory object.**
The chain's condense step reads `chat_history` whether it comes from memory or from input, so behavior within a conversation is unchanged.
Alternatives: `create_agent` with checkpointing (what the warning suggests) changes the RAG flow into agentic tool use, letting the model skip retrieval; rejected. `RunnableWithMessageHistory` adds a session store we don't need because Gradio already holds the history.

**Convert with `langchain_core.messages.convert_to_messages`, keeping only `role` and `content`.**
Gradio message dicts can carry extra keys (e.g. `metadata`); passing just `role`/`content` avoids conversion errors and yields `HumanMessage`/`AIMessage` objects the chain formats correctly.
Alternative: build `(human, ai)` tuples by pairing messages; more code and breaks on unpaired turns.

## Risks / Trade-offs

- [Gradio 6 delivers `content` as a list of parts instead of a string] → Confirmed during implementation: conversion does not fail, but the chain would render the raw list into the condense prompt. Mitigation applied: a `message_text` helper keeps only the text parts (non-text parts such as files are dropped) before converting.
- [Baseline drift] → Within a conversation results are identical; only cross-session leakage disappears. Record this when publishing baseline numbers.
- [A new `ConversationalRetrievalChain` deprecation warning may appear] → Expected and out of scope; addressed by a future rewrite.
