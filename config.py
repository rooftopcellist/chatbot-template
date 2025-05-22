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

# Supported file types
SUPPORTED_EXTENSIONS = ['.md', '.docx', '.pdf', '.csv', '.json', '.log', '.adoc', '.rst']

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
VERBOSE = False  # Enable verbose output including intermediate responses during query processing

# Repository settings
TRAINING_REPOS = [
    # Example configuration - uncomment to test with ansible-documentation:
    # {
    #     "url": "git@github.com:ansible/ansible-documentation.git",
    #     "name": "ansible-docs",  # Optional: custom directory name
    #     "branch": "devel"  # Optional: specific branch (defaults to default branch)
    # }
]  # List of repositories to automatically pull into training-data/

# Chat interface settings
CHATBOT_NAME = "Local Assistant"  # Name of the chatbot
WELCOME_MESSAGE = f"""Welcome to {CHATBOT_NAME}
A local chatbot that can answer questions based on your documents
Type 'exit' or 'quit' to end the session."""

# Web server settings
WEB_HOST = "127.0.0.1"  # Host to bind the web server to
WEB_PORT = 8080  # Port for the web server
WEB_DEBUG = True  # Enable debug mode for development
CORS_ORIGINS = ["*"]  # CORS origins for API access
