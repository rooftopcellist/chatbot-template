"""
Chat interface module for the terminal interface.
"""

from typing import List, Dict
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from query_engine import QueryEngine
import config

class ChatInterface:
    """
    Terminal-based chat interface for the chatbot.
    """

    def __init__(self, query_engine: QueryEngine):
        """
        Initialize the chat interface.

        Args:
            query_engine (QueryEngine): The query engine to use
        """
        self.query_engine = query_engine
        self.console = Console()
        self.history: List[Dict[str, str]] = []

    def display_welcome(self) -> None:
        """Display welcome message."""
        self.console.print(
            Panel.fit(
                f"[bold blue]{config.WELCOME_MESSAGE}[/bold blue]",
                title=config.CHATBOT_NAME,
                border_style="blue"
            )
        )

    def display_response(self, query: str, response: str) -> None:
        """
        Display a query and its response.

        Args:
            query (str): The user's query
            response (str): The chatbot's response
        """
        # Add to history
        self.history.append({
            "query": query,
            "response": response
        })

        # Display query
        self.console.print(
            Panel(
                f"[bold white]{query}[/bold white]",
                title="You",
                title_align="left",
                border_style="green"
            )
        )

        # Display response
        self.console.print(
            Panel(
                Markdown(response),
                title=config.CHATBOT_NAME,
                title_align="left",
                border_style="blue"
            )
        )

    def run(self) -> None:
        """Run the chat interface."""
        self.display_welcome()

        while True:
            # Get user input
            query = Prompt.ask("[bold green]You[/bold green]")

            # Check for exit command
            if query.lower() in ["exit", "quit"]:
                self.console.print("[bold blue]Goodbye![/bold blue]")
                break

            # Display processing message
            with self.console.status("[bold blue]Processing your query...[/bold blue]"):
                # Process query
                response = self.query_engine.query(query)

            # Display response
            self.display_response(query, response)
