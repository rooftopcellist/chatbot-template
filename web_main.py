"""
Web interface entry point for the chatbot application.
"""

import os
import sys
from rich.console import Console
from document_processor import load_documents
from embedding_engine import EmbeddingEngine
from query_engine import QueryEngine
from web_server import run_server
from repo_manager import RepoManager
import config


def main():
    """Main entry point for the web application."""
    console = Console()

    console.print(f"[bold blue]Starting {config.CHATBOT_NAME} Web Interface...[/bold blue]")

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

    # Check if the required model is available
    try:
        models_response = requests.get(f"{config.OLLAMA_BASE_URL}/api/tags")
        if models_response.status_code == 200:
            models = models_response.json().get("models", [])
            model_names = [model["name"] for model in models]

            if config.OLLAMA_MODEL not in model_names:
                console.print(f"[bold yellow]Model '{config.OLLAMA_MODEL}' not found.[/bold yellow]")
                console.print("Attempting to pull the model...")

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

    # Create training-data directory if it doesn't exist
    os.makedirs(config.DOCS_DIR, exist_ok=True)

    # Pull configured repositories
    console.print("Checking for configured repositories...")
    repo_manager = RepoManager(console)
    repo_success = repo_manager.pull_configured_repos()

    if not repo_success:
        console.print("[bold yellow]Warning: Some repository operations failed, but continuing with document loading...[/bold yellow]")

    # Load documents
    console.print(f"Loading documents from {config.DOCS_DIR}...")
    documents = load_documents()

    if not documents:
        console.print(f"[bold yellow]Warning: No documents found in {config.DOCS_DIR}[/bold yellow]")
        console.print("The chatbot will still work, but it won't have any context to draw from.")
        console.print(f"Add some documents to {config.DOCS_DIR} and restart to improve responses.")
    else:
        console.print(f"[bold green]Loaded {len(documents)} documents[/bold green]")

    # Initialize embedding engine
    console.print("Initializing embedding engine...")
    embedding_engine = EmbeddingEngine()

    # Load or create index
    console.print("Loading or creating index...")
    index = embedding_engine.load_or_create_index(documents)

    # Initialize query engine
    console.print("Initializing query engine...")
    query_engine = QueryEngine(index)

    # Start web server
    console.print("Starting web server...")
    console.print(f"[bold green]Web interface will be available at: http://{config.WEB_HOST}:{config.WEB_PORT}[/bold green]")
    console.print("[bold blue]Press Ctrl+C to stop the server[/bold blue]")

    try:
        run_server(query_engine)
    except KeyboardInterrupt:
        console.print("\n[bold blue]Shutting down web server...[/bold blue]")
    except Exception as e:
        console.print(f"[bold red]Error running web server: {str(e)}[/bold red]")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        console = Console()
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        console.print("[bold red]Traceback:[/bold red]")
        traceback.print_exc()
        sys.exit(1)
