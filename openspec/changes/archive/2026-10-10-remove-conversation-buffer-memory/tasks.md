## 1. Remove the memory object

- [x] 1.1 Delete the `ConversationBufferMemory` import and the `memory = ConversationBufferMemory(...)` line in `src/oracle/run_chat.py`; verify `grep ConversationBufferMemory src/oracle/run_chat.py` returns nothing
- [x] 1.2 Build the chain with `ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever)` (no `memory=`), leaving model, temperature and `k=10` untouched; verify with `git diff` that only the `memory=` argument changed on that line

## 2. Pass session history to the chain

- [x] 2.1 Import `convert_to_messages` from `langchain_core.messages` and, in `chat(question, history)`, convert `history` (keeping only `role` and `content`) into messages; verify `uv run python -c "import ast; ast.parse(open('src/oracle/run_chat.py').read())"` succeeds
- [x] 2.2 Invoke the chain with `{"question": question, "chat_history": chat_history}` and return `result["answer"]`; verify `legacy/run_chat.py` is unchanged with `git diff --quiet legacy/`
- [x] 2.3 Remove `type="messages"` from `gr.ChatInterface(...)` (Gradio 6 no longer accepts it); verify `uv run python -I -c "import inspect, gradio as gr; print('type' in inspect.signature(gr.ChatInterface.__init__).parameters)"` prints `False` and `grep 'type=' src/oracle/run_chat.py` returns nothing

## 3. Manual verification

- [x] 3.1 Run `uv run python src/oracle/run_chat.py` and confirm no `LangChainDeprecationWarning` mentions `ConversationBufferMemory` (a `ConversationalRetrievalChain` warning is expected and out of scope)
- [x] 3.2 In one browser tab ask a question, then a follow-up that refers to it (e.g. "tell me more"); confirm the follow-up is understood. If conversion fails because `content` is a list, apply the design.md mitigation and repeat
- [x] 3.3 Open a second tab and ask the same follow-up with no prior question; confirm it is not interpreted using the first tab's conversation
