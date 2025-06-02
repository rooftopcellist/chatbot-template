# Chatbot Developer Documentation

This directory contains comprehensive documentation about the chatbot system, its architecture, and best practices for using it effectively.

## Core Documentation

| Document | Description |
|----------|-------------|
| [Core Concepts](core-concepts.md) | High-level explanation of RAG chatbots and how they work |
| [Architecture](architecture.md) | Detailed explanation of the chatbot's components and data flow |
| [Tuning Pretrained Models](tuning-pretrained-models.md) | Guide to adjusting model parameters for optimal responses |
| [FAQ](faq.md) | Frequently asked questions about the chatbot system |

## Best Practices

| Document | Description |
|----------|-------------|
| [Optimizing Documentation](optimizing-documentation.md) | Best practices for creating documentation that works well with RAG |
| [Evaluating Performance](evaluating-performance.md) | Methods for assessing and improving chatbot performance |

## Configuration

| Document | Description |
|----------|-------------|
| [General Configuration](configuration/general-configuration.md) | Complete guide to customizing and configuring the chatbot system |
| [Repository Configuration](configuration/repo_configuration.md) | How to configure repositories that will be automatically pulled into the training data |

## Using This Documentation

These documents serve two purposes:

1. **Understanding the Chatbot**: Learn how the chatbot works, its architecture, and how to optimize it
2. **Example Content**: Serve as example content that you can use to test the chatbot

You can ask the chatbot questions about these documents to see how it retrieves and presents information. For example:
- "What is RAG and how does it work?"
- "How can I tune the model parameters?"
- "What's the architecture of the chatbot system?"
- "How should I structure my documentation for best results?"

## Adding Your Own Documentation

While this directory contains documentation about the chatbot itself, your actual team documentation should be placed in the `source-data` directory, which is the default location the chatbot uses to build its knowledge base.

See the [main README](../README.md) for more information on adding your team's documentation to the chatbot.
