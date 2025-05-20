"""
Configuration settings for the chatbot application.
"""

# Paths
DOCS_DIR = "training-data"  # Directory containing documents to index
INDEX_PERSIST_DIR = "data/index"  # Directory to store the persistent index

# Document processing
CHUNK_SIZE = 500  # Size of text chunks for embedding
CHUNK_OVERLAP = 50  # Overlap between chunks

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # HuggingFace model for embeddings

# LLM settings
OLLAMA_MODEL = "qwen3:1.7b"  # Default model to use
OLLAMA_BASE_URL = "http://localhost:11434"  # URL for the Ollama server

# Query settings
TOP_K = 5  # Number of chunks to retrieve for each query

# Chat interface settings
CHATBOT_NAME = "Local Assistant"  # Name of the chatbot
WELCOME_MESSAGE = f"""Welcome to {CHATBOT_NAME}
A local chatbot that can answer questions based on your documents
Type 'exit' or 'quit' to end the session."""
