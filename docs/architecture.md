---
title: "Chatbot Architecture and Flow"
description: "Detailed explanation of the chatbot's architecture, components, and data flow"
category: "reference"
tags: ["architecture", "design", "components", "flow", "technical"]
created: "2023-07-15"
updated: "2023-07-15"
---

# Chatbot Architecture and Flow

This document explains the architecture of the RAG chatbot, detailing each component's role and how data flows through the system.

## System Overview

The chatbot is built using a modular architecture with distinct components handling specific aspects of the RAG (Retrieval-Augmented Generation) process. The system follows a pipeline approach where data flows through several processing stages from document loading to response generation.

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Markdown Docs  │────▶│    Document     │────▶│    Embedding    │
│  (training-data)│     │    Processor    │     │     Engine      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Chat Interface │◀────│  Query Engine   │◀────│  Vector Index   │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲                        │                       ▲
        │                        ▼                       │
        │              ┌─────────────────┐               │
        │              │                 │               │
        └──────────────│  Ollama LLM     │───────────────┘
                       │  (qwen3:1.7b)   │
                       │                 │
                       └─────────────────┘
```

## Component Details

### 1. Document Processor

**File**: `document_processor.py`

**Purpose**: Loads and processes documents from the training data directory.

**Key Functions**:
- `load_documents()`: Recursively scans the training data directory for markdown files
- `process_markdown_file()`: Processes individual markdown files, extracting content and metadata

**Input**: Raw markdown files from the training-data directory
**Output**: List of Document objects with text content and metadata

**Flow**:
1. Scans the configured directory (default: `training-data/`)
2. For each markdown file:
   - Reads the file content
   - Extracts and parses YAML front matter (if present)
   - Creates a Document object with the content and metadata
3. Returns a list of all processed documents

### 2. Embedding Engine

**File**: `embedding_engine.py`

**Purpose**: Handles document chunking, embedding generation, and vector storage.

**Key Components**:
- `SentenceSplitter`: Chunks documents into smaller segments
- `HuggingFaceEmbedding`: Converts text chunks into vector embeddings
- `SimpleVectorStore`: Stores vector embeddings for efficient retrieval
- `VectorStoreIndex`: Provides indexing and search capabilities

**Input**: List of Document objects
**Output**: Vector store index for semantic search

**Flow**:
1. Checks if a persisted index exists
2. If an index exists:
   - Loads the index from disk
3. If no index exists:
   - Chunks documents into smaller segments using the SentenceSplitter
   - Converts each chunk into a vector embedding using the HuggingFace model
   - Creates a vector store index with these embeddings
   - Persists the index to disk for future use

**Configuration Parameters**:
- `CHUNK_SIZE`: Size of text chunks (default: 500)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50)
- `EMBEDDING_MODEL_NAME`: HuggingFace model for embeddings (default: "sentence-transformers/all-MiniLM-L6-v2")

### 3. Query Engine

**File**: `query_engine.py`

**Purpose**: Processes user queries and generates responses using the vector index and LLM.

**Key Components**:
- `Ollama`: Interface to the local LLM
- `Retriever`: Retrieves relevant document chunks from the vector index
- `CompactAndRefine`: Response synthesizer that refines responses based on retrieved context
- `RetrieverQueryEngine`: Combines retrieval and response generation

**Input**: User query (text) and vector index
**Output**: Generated response based on retrieved context

**Flow**:
1. Receives a user query
2. Converts the query into a vector embedding (internally)
3. Retrieves the most similar document chunks from the vector index
4. Constructs a prompt combining the query and retrieved chunks
5. Sends the prompt to the Ollama LLM
6. Returns the generated response

**Configuration Parameters**:
- `OLLAMA_MODEL`: Ollama model to use (default: "qwen3:1.7b")
- `OLLAMA_BASE_URL`: URL for the Ollama server (default: "http://localhost:11434")
- `TOP_K`: Number of chunks to retrieve for each query (default: 5)

### 4. Chat Interface

**File**: `chat_interface.py`

**Purpose**: Provides a terminal-based user interface for interacting with the chatbot.

**Key Components**:
- `Console`: Rich text console for formatted output
- `Panel`: UI component for displaying messages
- `Prompt`: Input component for getting user queries
- `Markdown`: Renderer for formatting responses

**Input**: User queries via terminal
**Output**: Formatted display of queries and responses

**Flow**:
1. Displays a welcome message
2. Enters a loop to:
   - Prompt for user input
   - Send the input to the query engine
   - Display the response
   - Repeat until the user exits

**Configuration Parameters**:
- `CHATBOT_NAME`: Name of the chatbot (default: "Local Assistant")
- `WELCOME_MESSAGE`: Welcome message to display

### 5. Main Application

**File**: `main.py`

**Purpose**: Orchestrates the overall application flow and initializes components.

**Key Functions**:
- Checks if Ollama is running
- Verifies if the required model is available
- Initializes all components
- Handles errors and exceptions

**Flow**:
1. Checks if Ollama is running and the required model is available
2. Creates necessary directories
3. Loads documents using the Document Processor
4. Initializes the Embedding Engine
5. Loads or creates the vector index
6. Initializes the Query Engine
7. Starts the Chat Interface

## Data Flow Through the System

### Initialization Phase

1. **Document Loading**:
   - Markdown files → Document Processor → List of Documents

2. **Index Creation**:
   - List of Documents → Embedding Engine → Vector Index
     - Documents → Chunking → Text Chunks
     - Text Chunks → Embedding Model → Vector Embeddings
     - Vector Embeddings → Vector Store → Vector Index

### Query Phase

1. **User Input**:
   - User → Chat Interface → Query Text

2. **Query Processing**:
   - Query Text → Query Engine → Response
     - Query Text → Vector Embedding
     - Vector Embedding → Vector Index → Relevant Chunks
     - Query + Relevant Chunks → Ollama LLM → Generated Response

3. **Response Display**:
   - Generated Response → Chat Interface → Formatted Output to User

## Key Technologies

1. **LlamaIndex**: Framework for building RAG applications
2. **HuggingFace Embeddings**: For converting text to vector embeddings
3. **Ollama**: For running the LLM locally
4. **Rich**: For the terminal user interface

## Configuration and Customization

The system is designed to be easily configurable through the `config.py` file, which contains settings for:

- Document directory path
- Index persistence directory
- Chunking parameters
- Embedding model selection
- LLM model selection
- Retrieval parameters
- UI customization

## Performance Considerations

- **Index Creation**: Creating the vector index is a one-time operation that can be resource-intensive for large document collections
- **Query Processing**: The speed of query processing depends on:
  - Size of the vector index
  - Complexity of the query
  - Speed of the LLM
- **Memory Usage**: The vector index is loaded into memory, so large document collections require more RAM

## Extension Points

The modular architecture allows for several extension points:

1. **Document Processor**: Add support for additional file formats (PDF, DOCX, etc.)
2. **Embedding Engine**: Use different embedding models or vector stores
3. **Query Engine**: Implement more sophisticated retrieval strategies
4. **Chat Interface**: Create a web or GUI interface instead of terminal

## Conclusion

The chatbot follows a clean, modular architecture that separates concerns and allows for easy customization and extension. The RAG approach combines the strengths of retrieval-based systems with the generative capabilities of LLMs, resulting in a chatbot that can provide accurate, contextual responses based on your team's documentation.
