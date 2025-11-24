# advanced-rag-chatbot
Retrieval Augmented Generation LLM Chatbot

## Accomplished
- [X] Weather Basic Agent
    - [X] Uses static/canned "it is sunny" weather `tool`.
- [ ] Weather Advanced Agent
    - [ ] Uses weather tool (`tool` learning)
    - [ ] Uses user location tool (`tool` learning)
    - [ ] Speaks in riddles (`responses` learning)
    - [ ] Uses a `SYSTEM_PROMPT`
    - [ ] Uses a `context_schema`
    - [ ] Uses `checkpoints`
- [X] Robust custom logging (python logger w pprint, blacklist, and noisy_list)
- [X] Create a dynamic model agent.
    - [X] set messages threshold to >1 to switch models. Got Claude AND Gemini working in 1 question.
- [ ] Add storage to advanced agent.

## Goals 

Build an Advanced RAG Chatbot (Single Agent)

### Objective

Build a self-contained application that answers questions based on a specific set of documents, maintaining conversation history.

### Setup

Load a small set of documents (e.g., three PDF articles on the A2A protocol).

### Embedding & Storage

Embed the documents and store them in a local Vector Store.

### Chain Construction

Create a chain using LCEL: Context + Question -> Retriever -> Formatted Prompt -> LLM -> Output.

### Refinement

Add ConversationBufferMemory to enable follow-up questions.

### Output

The chatbot should provide sourced answers only from the provided documents.
