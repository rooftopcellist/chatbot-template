# Source Data Directory

This directory is the default location for storing documents that will be used as source data for the RAG (Retrieval-Augmented Generation) system for the chatbot.

## Adding Documents

You can add any markdown (.md) files to this directory. The chatbot will automatically process them and build a vector index for retrieval.

## Document Format

For best results, follow these guidelines:

1. Use clear, descriptive filenames
2. Structure your documents with proper markdown headings
3. Include YAML front matter at the top of each file (optional but recommended)
4. Keep each document focused on a specific topic

## YAML Front Matter Example

```yaml
---
title: "Document Title"
description: "Brief description of the document"
category: "category-name"
tags: ["tag1", "tag2", "tag3"]
created: "2023-06-15"
updated: "2023-06-20"
---
```

## Directory Organization

You can organize your documents in subdirectories if you have many files. The chatbot will recursively scan all subdirectories for markdown files.

Example structure:
```
source-data/
├── README.md
├── product-documentation/
│   ├── installation.md
│   ├── configuration.md
│   └── troubleshooting.md
├── api-reference/
│   ├── endpoints.md
│   └── authentication.md
└── tutorials/
    ├── getting-started.md
    └── advanced-usage.md
```

## Rebuilding the Index

After adding new documents or modifying existing ones, you'll need to rebuild the vector index:

1. Delete the existing index: `rm -rf data/index`
2. Run the chatbot again: `python main.py`

The system will automatically rebuild the index with the new documents.

## Tips for Better Results

1. **Be specific**: The more specific and clear your documents are, the better the chatbot will be able to retrieve relevant information.

2. **Use proper headings**: Structure your documents with clear headings (# for main headings, ## for subheadings, etc.) to help with chunking and retrieval.

3. **Include examples**: Concrete examples help the model understand the context better.

4. **Keep documents focused**: Each document should focus on a specific topic rather than covering many different topics.

5. **Update regularly**: Keep your documents up-to-date to ensure the chatbot provides accurate information.
