# Simpole RAG Chatbot Template

A ready-to-use template for creating a local chatbot that can answer questions about your team's documentation using Retrieval-Augmented Generation (RAG). This tool helps teams make their internal knowledge more accessible and reduces the time spent searching through documentation.

## Why Use This Template?

- **Knowledge Accessibility**: Make team documentation easily accessible through natural language questions
- **Reduce Onboarding Time**: Help new team members quickly find answers to common questions
- **Offline Operation**: Runs completely locally without sending your data to external APIs
- **Privacy-Preserving**: Your sensitive team documents never leave your machine
- **Customizable**: Easily adapt to your team's specific documentation and needs

## Features

- Loads Markdown files from a specified directory
- Strips YAML front matter
- Chunks the text for semantic embedding
- Embeds the content using a Hugging Face model
- Stores the embeddings in a vector index locally
- Provides a terminal interface for asking questions
- Retrieves relevant document chunks
- Sends the chunks + question to the model via Ollama
- Returns relevant answers
- Persists the index to avoid rebuilding it every time
- Runs entirely offline

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
   source venv/bin/activate  # On Windows: venv\Scripts\activate
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

2. Add your team's markdown documents to the `training-data` directory:
   ```
   cp -r your-team-docs/* training-data/
   ```

3. Run the chatbot:
   ```
   python main.py
   # Or use the convenience script
   ./run.sh
   ```

4. Ask questions about your team's documentation in the terminal interface.

### Example Questions You Can Ask

Once your team's documentation is loaded, you can ask questions like:

- "What's our process for code reviews?"
- "How do I set up my development environment?"
- "What are the steps to deploy to production?"
- "Who should I contact for access to the staging environment?"
- "What's our policy on handling customer data?"
- "What's the architecture of our authentication system?"
- "What are the required fields for the user API endpoint?"
- "How do we handle error logging in the application?"

### Team Usage Scenarios

- **New Employee Onboarding**: Help new team members quickly find information without having to ask colleagues repeatedly
- **Cross-Team Collaboration**: Enable team members to find information about other teams' systems and processes
- **Remote Work Support**: Provide 24/7 access to team knowledge regardless of time zones
- **Knowledge Preservation**: Capture and make searchable the knowledge of departing team members
- **Meeting Preparation**: Quickly look up relevant information before meetings
- **Technical Support**: Help support teams find solutions to common problems

## Configuration

You can modify the settings in `config.py`:

- `DOCS_DIR`: Path to the directory containing Markdown files
- `INDEX_PERSIST_DIR`: Directory to store the persistent index
- `SYSTEM_PROMPT_PATH`: Path to the system prompt file
- `CHUNK_SIZE`: Size of text chunks for embedding
- `CHUNK_OVERLAP`: Overlap between chunks
- `EMBEDDING_MODEL_NAME`: Hugging Face model for embeddings
- `OLLAMA_MODEL`: Ollama model to use
- `OLLAMA_BASE_URL`: URL for the Ollama server
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
├── docs/                     # Example documentation structure and system docs
│   ├── README.md             # Documentation index with links to all docs
│   ├── core-concepts.md      # High-level explanation of RAG chatbots
│   ├── architecture.md       # System architecture and component details
│   ├── tuning-pretrained-models.md # Guide to adjusting model parameters
│   ├── optimizing-documentation.md # Best practices for documentation
│   ├── evaluating-performance.md   # Methods for assessing chatbot performance
│   ├── guides/               # Step-by-step guides
│   ├── reference/            # Technical reference documentation
│   ├── tutorials/            # Comprehensive tutorials
│   ├── examples/             # Code examples and use cases
│   └── api/                  # API documentation
└── training-data/            # Default directory for training documents
```

## Adding Your Team's Documentation

The `training-data/` directory is where you'll add your team's documentation for the chatbot to learn from. The system works best with well-structured markdown files.

### Types of Documentation You Can Include

- **Onboarding Materials**: Team processes, workflows, and getting started guides
- **Technical Documentation**: Architecture diagrams, API references, and code explanations
- **Policies and Procedures**: Company policies, security protocols, and standard procedures
- **FAQs and Troubleshooting**: Common issues and their solutions
- **Project Documentation**: Project overviews, requirements, and specifications
- **Meeting Notes and Decisions**: Important decisions and their context
- **Knowledge Base Articles**: How-to guides and explanations of complex topics
- **Team Wikis**: Team structure, responsibilities, and contact information

### Adding Documents

1. Create markdown (.md) files with your content

2. Place the files in the `training-data/` directory, organizing with subdirectories as needed. Below is a potential structure, you can alternatively clone your existing docs repo into the `training-data/` directory.
   ```
   training-data/
   ├── onboarding/
   │   ├── first-day-setup.md
   │   └── team-tools.md
   ├── technical/
   │   ├── architecture-overview.md
   │   └── api-documentation.md
   ├── processes/
   │   ├── code-review-process.md
   │   └── deployment-process.md
   └── faqs/
       ├── common-issues.md
       └── troubleshooting.md
   ```
> Note: 2. Add YAML front matter at the top of each file to improve organization and searchability:
> ```yaml
> ---
> title: "Document Title"
> description: "Brief description of what this document covers"
> category: "technical-docs"  # Helps with organization
> tags: ["api", "authentication", "oauth"]  # Relevant keywords
> created: "2023-06-15"
> updated: "2023-06-20"
> author: "Jane Smith"  # Optional
> team: "Backend"  # Optional
> priority: "high"  # Optional
> ---
> ```

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

1. Delete the existing index:
   ```
   rm -rf data/index
   ```

2. Run the chatbot again to rebuild the index.

### Limitations to Be Aware Of

- The chatbot can currentlyonly answer based on information in your documents
- It may occasionally provide incomplete or inaccurate information
- Complex, nuanced topics might require human expertise
- The quality of answers depends on the quality of your documentation
- Very large document collections may require more powerful hardware
- The chatbot does not have access to real-time information or external data sources

## Acknowledgements

- [LlamaIndex](https://www.llamaindex.ai/) for the RAG framework
- [Ollama](https://ollama.ai/) for the local LLM hosting
- [Hugging Face](https://huggingface.co/) for the embedding models
