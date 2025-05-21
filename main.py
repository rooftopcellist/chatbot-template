"""
Main entry point for the chatbot application.
"""

import os
from rich.console import Console
from document_processor import load_documents
from embedding_engine import EmbeddingEngine
from query_engine import QueryEngine
from chat_interface import ChatInterface
import config

def main():
    """Main entry point for the application."""
    console = Console()

    console.print(f"[bold blue]Starting {config.CHATBOT_NAME}...[/bold blue]")

    # Check if Ollama is running
    console.print("Checking if Ollama is running...")
    try:
        import requests
        response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags")
        if response.status_code != 200:
            console.print("[bold red]Error: Ollama server is not responding.[/bold red]")
            console.print(f"Make sure Ollama is running at {config.OLLAMA_BASE_URL}")
            return
        else:
            console.print("[bold green]Ollama is running.[/bold green]")
    except Exception as e:
        console.print("[bold red]Error: Could not connect to Ollama server.[/bold red]")
        console.print(f"Error details: {e}")
        console.print(f"Make sure Ollama is running at {config.OLLAMA_BASE_URL}")
        return

    # Check if the model is available
    try:
        response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags")
        models = [model["name"] for model in response.json().get("models", [])]
        if config.OLLAMA_MODEL not in models:
            console.print(f"[bold yellow]Warning: Model '{config.OLLAMA_MODEL}' not found in Ollama.[/bold yellow]")
            console.print(f"Available models: {', '.join(models)}")
            console.print(f"Pulling the model now. This may take a few minutes...")

            # Pull the model
            try:
                pull_response = requests.post(
                    f"{config.OLLAMA_BASE_URL}/api/pull",
                    json={"name": config.OLLAMA_MODEL}
                )
                if pull_response.status_code == 200:
                    console.print(f"[bold green]Successfully pulled model '{config.OLLAMA_MODEL}'.[/bold green]")
                else:
                    console.print(f"[bold red]Failed to pull model. Status code: {pull_response.status_code}[/bold red]")
                    console.print(f"You may need to run manually: ollama pull {config.OLLAMA_MODEL}")
                    return
            except Exception as e:
                console.print(f"[bold red]Error pulling model: {str(e)}[/bold red]")
                console.print(f"You may need to run manually: ollama pull {config.OLLAMA_MODEL}")
                return
    except Exception as e:
        console.print(f"[bold yellow]Warning: Could not check available models: {str(e)}[/bold yellow]")

    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(config.INDEX_PERSIST_DIR), exist_ok=True)

    # Initialize components
    console.print(f"[bold blue]Initializing {config.CHATBOT_NAME}...[/bold blue]")

    # Load documents
    console.print("Loading documents...")
    documents = load_documents()

    if not documents:
        console.print(f"[bold red]Error: No documents found in {config.DOCS_DIR}[/bold red]")
        console.print("Please make sure the directory exists and contains supported document files.")
        console.print("Supported file types: .md, .docx, .pdf, .csv, .json, .log, .adoc")
        return

    # Initialize embedding engine
    console.print("Initializing embedding engine...")
    embedding_engine = EmbeddingEngine()

    # Load or create index
    console.print("Loading or creating index...")
    index = embedding_engine.load_or_create_index(documents)

    # Initialize query engine
    console.print("Initializing query engine...")
    query_engine = QueryEngine(index)

    # Initialize chat interface
    console.print("Starting chat interface...")
    chat_interface = ChatInterface(query_engine)

    # Run chat interface
    chat_interface.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        console = Console()
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        console.print("[bold red]Traceback:[/bold red]")
        traceback.print_exc()
