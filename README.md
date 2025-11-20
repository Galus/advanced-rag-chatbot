# advanced-rag-chatbot
Retrieval Augmented Generation LLM Chatbot

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
