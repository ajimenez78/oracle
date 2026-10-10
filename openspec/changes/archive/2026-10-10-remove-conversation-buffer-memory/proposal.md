## Why

`src/oracle/run_chat.py` builds a `ConversationBufferMemory`, which LangChain deprecated in 0.3.1 and will remove in 2.0.0; every start emits a `LangChainDeprecationWarning`. The same object is also a known PoC defect (SPEC section 10): one global, in-memory buffer shared by every browser session, so conversations leak into each other.

## What Changes

- Remove `ConversationBufferMemory` (import and instance) from `run_chat.py`.
- Build `ConversationalRetrievalChain` without `memory=`.
- In `chat(question, history)`, convert the history Gradio already passes into LangChain messages and send it to the chain as `chat_history`.
- Conversation history becomes scoped to each Gradio session instead of shared globally.
- Drop the `type="messages"` argument from `gr.ChatInterface`: Gradio 6 removed it (messages is the only format) and the app crashes with a `TypeError` at startup, which blocks verifying this change.

Non-goals:
- Replacing `ConversationalRetrievalChain` (itself deprecated) with plain composition or the OpenAI SDK.
- Changing prompts, model, temperature or retrieval settings (k=10); the RAG baseline stays as is.
- Fixing other unrelated warnings.

## Capabilities

### New Capabilities
- `legacy-chat`: conversation history handling of the PoC chat (`run_chat.py`), scoped to the user's session.

### Modified Capabilities
<!-- none: no specs exist yet under openspec/specs/ -->

## Impact

- Code: `src/oracle/run_chat.py` only. `legacy/run_chat.py` stays untouched as the read-only reference.
- Dependencies: none added; `langchain_core` (already installed via `langchain-classic`/`langchain-openai`) provides `convert_to_messages`.
- Baseline: answers within one conversation are unchanged; across sessions, history no longer leaks. Note this when recording baseline numbers.
