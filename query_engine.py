"""
Query engine module for handling queries and generating responses.
"""

from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.core.response_synthesizers import CompactAndRefine
from llama_index.core.query_engine import RetrieverQueryEngine
import config

class QueryEngine:
    """
    Handles query processing and response generation.
    """

    def __init__(self, index: VectorStoreIndex):
        """
        Initialize the query engine.

        Args:
            index (VectorStoreIndex): The vector store index to query
        """
        self.index = index

        # Initialize Ollama LLM
        self.llm = Ollama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            request_timeout=300.0,  # Increased timeout for smaller models which might be slower
            temperature=0.1,  # Lower temperature for more focused responses
            num_ctx=4096,  # Context window size
            num_predict=1024,  # Maximum number of tokens to generate
            repeat_penalty=1.1  # Penalty for repeating tokens
        )

        # Create retriever
        self.retriever = self.index.as_retriever(
            similarity_top_k=config.TOP_K
        )

        # Create response synthesizer
        self.response_synthesizer = CompactAndRefine(
            llm=self.llm,
            verbose=True
        )

        # Create query engine
        self.query_engine = RetrieverQueryEngine(
            retriever=self.retriever,
            response_synthesizer=self.response_synthesizer
        )

    def query(self, query_text: str) -> str:
        """
        Process a query and generate a response.

        Args:
            query_text (str): The query text

        Returns:
            str: The generated response
        """
        try:
            # Execute query
            response = self.query_engine.query(query_text)

            # Return response text
            return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"
