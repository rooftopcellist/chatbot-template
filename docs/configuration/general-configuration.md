---
title: "General Configuration Guide"
description: "Guide to customizing and configuring the chatbot system"
category: "configuration"
tags: ["configuration", "customization", "llm", "system-prompt", "parameters"]
created: "2025-05-21"
created: "2025-05-21"
---

# General Configuration Guide

This guide covers all the ways you can customize and configure the chatbot to meet your specific needs.

## Customizing the System Prompt

The chatbot uses a system prompt to guide its responses. By default, it's configured as a documentation and code assistant with expertise in Python and Ansible.

You can customize the system prompt by editing the `system_prompt.txt` file in the root directory. This allows you to:

- Change the chatbot's personality and tone
- Add specific expertise areas
- Provide guidelines for how responses should be formatted
- Include examples of ideal responses

The system prompt is loaded when the chatbot starts and is passed to the LLM to guide its behavior.

## Adjusting LLM Parameters

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

## Controlling Verbose Output

You can control whether the chatbot displays intermediate processing steps during query processing:

```python
# Query settings
VERBOSE = False  # Set to True to see intermediate responses and processing steps
```

- **VERBOSE = False** (default): Clean output with only the final response
- **VERBOSE = True**: Shows intermediate processing steps, useful for debugging or understanding how responses are generated

See [Tuning Pretrained Models](../tuning-pretrained-models.md) for detailed guidance on parameter tuning.

## Using a Different LLM

To use a different Ollama model:

1. Pull the model with Ollama:
   ```
   ollama pull mistral:7b-instruct
   ```

2. Update the `OLLAMA_MODEL` in `config.py`:
   ```python
   OLLAMA_MODEL = "mistral:7b-instruct"
   ```

## Changing the Embedding Model

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

## Additional Configuration Options

### Document Processing Settings

```python
# Document processing
CHUNK_SIZE = 500  # Size of text chunks for embedding
CHUNK_OVERLAP = 50  # Overlap between chunks
```

### Query Settings

```python
# Query settings
TOP_K = 5  # Number of chunks to retrieve for each query
```

### Chat Interface Settings

```python
# Chat interface settings
CHATBOT_NAME = "Local Assistant"  # Name of the chatbot
WELCOME_MESSAGE = f"""Welcome to {CHATBOT_NAME}
A local chatbot that can answer questions based on your documents
Type 'exit' or 'quit' to end the session."""
```

### File Type Support

```python
# Supported file types
SUPPORTED_EXTENSIONS = ['.md', '.docx', '.pdf', '.csv', '.json', '.log', '.adoc', '.rst']
```
