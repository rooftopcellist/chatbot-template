# Frequently Asked Questions

## What is the purpose of the document parsing logic in document_processor.py? Why different parsing logic for each file type?

Document parsing logic varies by file type because each format stores content differently. The purpose is to extract clean, usable text from various file formats for the RAG system.

Different file types require specialized handling:

* Markdown files need frontmatter extraction
* PDFs require page-by-page text extraction
* DOCX files need paragraph extraction
* CSV/JSON files need structured data conversion to text
* RST/AsciiDoc files have special formatting to handle

The [document_processor.py](../document_processor.py) module handles this by:

1. Identifying file types by extension
2. Routing each file to the appropriate processor function
3. Extracting text content and relevant metadata
4. Converting everything to a standard  Document object format

This standardization is crucial because the embedding engine needs plain text to create vector embeddings. Without proper parsing, the RAG system would either fail to process certain files or create poor-quality embeddings that lead to irrelevant retrieval results.

## When would it make sense to add an MCP? Give an example.

It would make sense to add an MCP when you want to extend the chatbot's capabilities with external tools or AI services while maintaining user control over model access.

For example, you could implement an MCP to:

1. Allow the chatbot to request specialized calculations or data processing from external tools when your documentation doesn't contain the answer.
2. Enable the chatbot to handle complex queries by delegating to specialized AI models (like code generation or image analysis) while letting users maintain control over which models are used.

A practical implementation might look like:
- Adding a calculator tool that uses sampling to solve math problems not covered in your docs
- Implementing a code generation tool that can create example scripts based on your documentation
- Creating a document analyzer that can process and summarize new files users upload during chat


## How could I make it possible for the chatbot query GitHub for information that isn't in the documents?

You could implement a tool that uses the GitHub API to search for relevant information. This tool could be triggered when the chatbot detects that the user's query requires external knowledge. The tool would then query the GitHub API and return the results to the chatbot, which could then use this information to generate a response.
