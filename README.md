# RAG Chatbot Template

A ready-to-use template for creating a local chatbot that can answer questions about your team's documentation using Retrieval-Augmented Generation (RAG).

You can train the chatbot on various document formats including markdown, PDF, Word documents, CSV, JSON, log files, and AsciiDoc that you find useful and then ask questions about them.

## Requirements

- Python 3.8+
- Ollama with qwen3:1.7b model installed

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/chatbot-template.git
   cd chatbot-template
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install Ollama and pull the qwen3:1.7b model:
   ```
   # Install Ollama from https://ollama.ai/
   ollama pull qwen3:1.7b
   ```

## Usage

### Basic Setup and Running

1. Make sure Ollama is running:
   ```
   ollama serve
   ```

2. Add your team's documents to the `training-data` directory. The chatbot supports multiple file formats (.md, .docx, .pdf, .csv, .json, .log, .adoc). You can also clone your existing docs repo into the `training-data` directory (see [Repository Configuration](configuration/repo_configuration.md)). Or you can use the sample documentation provided in the `sample-docs` directory to test out this chatbot:
   ```
   cp -r sample-docs/* training-data/
   cp -r docs/* training-data/
   ```

> Note: This will include info about the chatbot itself in the training data. Skip this step if you don't want this.

3. Run the chatbot:
   ```
   ./run.sh

   # Or run main.py directly
   python main.py

   # To force recreation of the index (useful after adding new documents)
   ./run.sh --refresh
   ```

4. Ask questions about your team's documentation in the terminal interface.

5. Try asking a question about the documentation you just added. If you are using the sample docs, try asking it, "What is RAG and how does it work?", or "What is a fact about Stradivarius?".

## Configuration

You can modify the settings in `config.py`:

- `DOCS_DIR`: Path to the directory containing document files
- `INDEX_PERSIST_DIR`: Directory to store the persistent index
- `SYSTEM_PROMPT_PATH`: Path to the system prompt file
- `CHUNK_SIZE`: Size of text chunks for embedding
- `CHUNK_OVERLAP`: Overlap between chunks
- `EMBEDDING_MODEL_NAME`: Hugging Face model for embeddings
- `OLLAMA_MODEL`: Ollama model to use
- `OLLAMA_BASE_URL`: URL for the Ollama server
- `OLLAMA_TEMPERATURE`: Controls randomness (0.0 = deterministic, 1.0 = creative)
- `OLLAMA_NUM_CTX`: Context window size in tokens
- `OLLAMA_NUM_PREDICT`: Maximum number of tokens to generate
- `OLLAMA_REPEAT_PENALTY`: Penalty for repeating tokens
- `OLLAMA_REQUEST_TIMEOUT`: Timeout in seconds for Ollama requests
- `TOP_K`: Number of chunks to retrieve for each query
- `CHATBOT_NAME`: Name of the chatbot
- `WELCOME_MESSAGE`: Welcome message to display

## Directory Structure

```
chatbot-template/
├── config.py                 # Configuration settings
├── main.py                   # Main application entry point
├── document_processor.py     # Document loading and processing
├── embedding_engine.py       # Embedding and vector storage
├── query_engine.py           # Query processing and response generation
├── chat_interface.py         # Terminal chat interface
├── system_prompt.txt         # System prompt for guiding the chatbot's responses
├── run.sh                    # Convenience script to run the chatbot
├── requirements.txt          # Python dependencies
├── data/                     # Directory for storing data
│   └── index/                # Persistent vector index
└── training-data/            # Default directory for training documents
```

## Adding Your Team's Documentation

The `training-data/` directory is where you'll add your team's documentation for the chatbot to learn from. The system works best with well-structured markdown files.

### Types of Documentation You Can Include

Supported file types:
* Markdown (.md)
* PDF (.pdf)
* Word documents (.docx)
* JSON (.json)
* CSV (.csv)
* Text (.txt)
* AsciiDoc (.adoc)
* reStructuredText (.rst)

Coming Soon:
* Jinja2 (.j2)
* HTML (.html)
* YAML (.yaml)
* XML (.xml)
* Images (.jpg, .png, .gif)
* Videos (.mp4, .avi)
* Audio (.mp3, .wav)
* Powerpoint (.pptx)

- **Onboarding Materials**: Team processes, workflows, and getting started guides
- **Technical Documentation**: Architecture diagrams, API references, and code explanations
- **Policies and Procedures**: Company policies, security protocols, and standard procedures
- **FAQs and Troubleshooting**: Common issues and their solutions
- **Project Documentation**: Project overviews, requirements, and specifications
- **Meeting Notes and Decisions**: Important decisions and their context
- **Knowledge Base Articles**: How-to guides and explanations of complex topics
- **Team Wikis**: Team structure, responsibilities, and contact information
- **Common Slack Questions**: Questions that are frequently asked in Slack channels
- **Internal Tools Documentation**: Documentation for internal tools and services
- Be Creative!

### Adding Documents

1. Create files in any of the supported formats:
   - Markdown (.md) - with optional YAML front matter
   - Word documents (.docx)
   - PDF files (.pdf)
   - CSV files (.csv)
   - JSON files (.json)
   - Log files (.log)
   - AsciiDoc files (.adoc)
   - reStructuredText files (.rst)

2. Place the files in the `training-data/` directory, organizing with subdirectories as needed. You can alternatively clone your existing docs repo into the `training-data/` directory.

3. Run the chatbot to build or rebuild the index:
   ```
   python main.py
   ```

## System Documentation

The `docs/` directory contains comprehensive documentation about the chatbot system itself:

- [Core Concepts](docs/core-concepts.md): High-level explanation of RAG chatbots and how they work
- [Architecture](docs/architecture.md): Detailed explanation of the chatbot's components and data flow
- [Tuning Pretrained Models](docs/tuning-pretrained-models.md): Guide to adjusting model parameters for optimal responses
- [Optimizing Documentation](docs/optimizing-documentation.md): Best practices for creating documentation that works well with RAG
- [Evaluating Performance](docs/evaluating-performance.md): Methods for assessing and improving chatbot performance
- [FAQ](docs/faq.md): Frequently asked questions about the chatbot system

See the [docs README](docs/README.md) for a complete index of all documentation.

## Customizing the Chatbot

### Customizing the System Prompt

The chatbot uses a system prompt to guide its responses. By default, it's configured as a documentation and code assistant with expertise in Python and Ansible.

You can customize the system prompt by editing the `system_prompt.txt` file in the root directory. This allows you to:

- Change the chatbot's personality and tone
- Add specific expertise areas
- Provide guidelines for how responses should be formatted
- Include examples of ideal responses

The system prompt is loaded when the chatbot starts and is passed to the LLM to guide its behavior.

### Adjusting LLM Parameters

You can fine-tune the behavior of the language model by adjusting parameters in `config.py`:

```python
# LLM settings
OLLAMA_MODEL = "qwen3:1.7b"  # Default model to use
OLLAMA_TEMPERATURE = 0.1  # Controls randomness (0.0 = deterministic, 1.0 = creative)
OLLAMA_NUM_CTX = 4096  # Context window size
OLLAMA_NUM_PREDICT = 1024  # Maximum number of tokens to generate
OLLAMA_REPEAT_PENALTY = 1.1  # Penalty for repeating tokens
```

- **Temperature**: Lower values (0.0-0.3) for factual, consistent responses; higher values (0.5-0.8) for more creative responses
- **Context Window**: Increase for handling more context from retrieved documents
- **Max Tokens**: Adjust based on how detailed you want responses to be
- **Repeat Penalty**: Increase to reduce repetition in responses

### Controlling Verbose Output

You can control whether the chatbot displays intermediate processing steps during query processing:

```python
# Query settings
VERBOSE = False  # Set to True to see intermediate responses and processing steps
```

- **VERBOSE = False** (default): Clean output with only the final response
- **VERBOSE = True**: Shows intermediate processing steps, useful for debugging or understanding how responses are generated

See [Tuning Pretrained Models](docs/tuning-pretrained-models.md) for detailed guidance on parameter tuning.

### Using a Different LLM

To use a different Ollama model:

1. Pull the model with Ollama:
   ```
   ollama pull mistral:7b-instruct
   ```

2. Update the `OLLAMA_MODEL` in `config.py`:
   ```python
   OLLAMA_MODEL = "mistral:7b-instruct"
   ```

### Changing the Embedding Model

To use a different embedding model:

1. Update the `EMBEDDING_MODEL_NAME` in `config.py`:
   ```python
   EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
   ```

2. Delete the existing index to force a rebuild:
   ```
   ./run.sh --refresh
   ```

   Or manually:
   ```
   rm -rf data/index
   ```

## Troubleshooting

### Ollama Connection Issues

If you see an error connecting to Ollama:

1. Make sure Ollama is running:
   ```
   ollama serve
   ```

2. Check if the model is available:
   ```
   ollama list
   ```

3. Pull the model if it's not available:
   ```
   ollama pull qwen3:1.7b
   ```

### Index Building Issues

If you have issues with the index:

1. Use the --refresh flag to automatically delete and rebuild the index:
   ```
   ./run.sh --refresh
   ```

2. Or manually delete the existing index:
   ```
   rm -rf data/index
   ```

3. Run the chatbot again to rebuild the index.

## Features

- Loads multiple document formats (.md, .docx, .pdf, .csv, .json, .log, .adoc, .rst) from a specified directory
- Extracts text content from each file type appropriately
- Strips YAML front matter from Markdown files
- Chunks the text for semantic embedding
- Embeds the content using a Hugging Face model
- Stores the embeddings in a vector index locally
- Provides a terminal interface for asking questions
- Retrieves relevant document chunks
- Sends the chunks + question to the model via Ollama
- Returns relevant answers
- Persists the index to avoid rebuilding it every time
- Runs entirely offline

## Limitations to Be Aware Of

- The chatbot can currently only answer based on information in your documents
- It may occasionally provide incomplete or inaccurate information
- Complex, nuanced topics might require human expertise
- The quality of answers depends on the quality of your documentation
- Very large document collections may require more powerful hardware
- The chatbot does not have access to real-time information or external data sources

## Acknowledgements

- [LlamaIndex](https://www.llamaindex.ai/) for the RAG framework
- [Ollama](https://ollama.ai/) for the local LLM hosting
- [Hugging Face](https://huggingface.co/) for the embedding models
