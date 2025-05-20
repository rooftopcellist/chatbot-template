"""
Document processor module for loading and processing documents.
"""

import os
import frontmatter
from typing import List, Dict, Any
from llama_index.core.schema import Document
import config

def load_documents() -> List[Document]:
    """
    Load all supported documents from the configured directory.
    Currently supports Markdown files with optional YAML front matter.
    
    Returns:
        List[Document]: List of processed documents
    """
    documents = []

    # Ensure the docs directory exists
    if not os.path.exists(config.DOCS_DIR):
        print(f"Warning: Documents directory '{config.DOCS_DIR}' not found.")
        return documents

    # Walk through the directory and process all .md files
    for root, _, files in os.walk(config.DOCS_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    # Process the file
                    doc = process_markdown_file(file_path)
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    print(f"Loaded {len(documents)} documents from {config.DOCS_DIR}")
    return documents

def process_markdown_file(file_path: str) -> Document:
    """
    Process a single Markdown file.
    Strips YAML front matter if present.

    Args:
        file_path (str): Path to the Markdown file

    Returns:
        Document: Processed document
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        # Parse frontmatter
        post = frontmatter.load(f)

        # Extract content without frontmatter
        content = post.content

        # Create metadata
        metadata = {
            'source': file_path,
            'filename': os.path.basename(file_path),
            'filetype': 'markdown',
            **post.metadata  # Include frontmatter as metadata
        }

        # Create Document object
        return Document(text=content, metadata=metadata)
