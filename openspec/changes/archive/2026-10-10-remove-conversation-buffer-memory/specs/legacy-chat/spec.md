## Purpose

Defines how the PoC chat keeps conversation history, so follow-up questions are understood within a conversation without leaking context between users or sessions.

## ADDED Requirements

### Requirement: Conversation history is scoped to the session
The chat SHALL use only the current session's prior messages as conversation history when answering a question. It MUST NOT keep conversation history in any process-wide state shared between sessions.

#### Scenario: First question in a session
- **WHEN** a user asks a question in a session with no prior messages
- **THEN** the chat answers using no conversation history

#### Scenario: Follow-up question in the same session
- **WHEN** a user asks a follow-up question that refers to an earlier message in the same session
- **THEN** the chat uses that session's earlier messages to interpret the follow-up

#### Scenario: Two independent sessions
- **WHEN** two sessions are open at the same time and a user asks a question in the second session
- **THEN** the chat does not use any message from the first session as history

### Requirement: No deprecated memory warning at startup
Starting the chat SHALL NOT emit a deprecation warning about the conversation memory component.

#### Scenario: Chat starts
- **WHEN** the chat application is started
- **THEN** no `LangChainDeprecationWarning` mentioning `ConversationBufferMemory` is emitted
