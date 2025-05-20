"""
Configuration settings for the chatbot application.
"""

# Paths
DOCS_DIR = "training-data"  # Directory containing documents to index
INDEX_PERSIST_DIR = "data/index"  # Directory to store the persistent index
SYSTEM_PROMPT_PATH = "system_prompt.txt"  # Path to the system prompt file

# Document processing
CHUNK_SIZE = 500  # Size of text chunks for embedding
CHUNK_OVERLAP = 50  # Overlap between chunks

# Embedding model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # HuggingFace model for embeddings

# LLM settings
OLLAMA_MODEL = "qwen3:1.7b"  # Default model to use
OLLAMA_BASE_URL = "http://localhost:11434"  # URL for the Ollama server
OLLAMA_TEMPERATURE = 0.1  # Controls randomness (0.0 = deterministic, 1.0 = creative)
OLLAMA_NUM_CTX = 4096  # Context window size
OLLAMA_NUM_PREDICT = 1024  # Maximum number of tokens to generate
OLLAMA_REPEAT_PENALTY = 1.1  # Penalty for repeating tokens
OLLAMA_REQUEST_TIMEOUT = 300.0  # Timeout in seconds

# Query settings
TOP_K = 5  # Number of chunks to retrieve for each query

# Chat interface settings
CHATBOT_NAME = "Local Assistant"  # Name of the chatbot
WELCOME_MESSAGE = f"""Welcome to {CHATBOT_NAME}
A local chatbot that can answer questions based on your documents
Type 'exit' or 'quit' to end the session."""
