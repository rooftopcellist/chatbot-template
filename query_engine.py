"""
Query engine module for handling queries and generating responses.
"""

import os
from llama_index.core import VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.core.response_synthesizers import CompactAndRefine
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.prompts import PromptTemplate
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

        # Load system prompt if it exists
        system_prompt = ""
        if os.path.exists(config.SYSTEM_PROMPT_PATH):
            with open(config.SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
            print(f"Loaded system prompt from {config.SYSTEM_PROMPT_PATH}")
        else:
            print(f"Warning: System prompt file not found at {config.SYSTEM_PROMPT_PATH}")

        # Initialize Ollama LLM
        self.llm = Ollama(
            model=config.OLLAMA_MODEL,
            base_url=config.OLLAMA_BASE_URL,
            request_timeout=config.OLLAMA_REQUEST_TIMEOUT,
            temperature=config.OLLAMA_TEMPERATURE,
            num_ctx=config.OLLAMA_NUM_CTX,
            num_predict=config.OLLAMA_NUM_PREDICT,
            repeat_penalty=config.OLLAMA_REPEAT_PENALTY,
            system_prompt=system_prompt
        )

        # Create retriever
        self.retriever = self.index.as_retriever(
            similarity_top_k=config.TOP_K
        )

        # Create custom prompt template for response generation
        qa_template_str = (
            "You are a documentation and code assistant with expertise in Python and Ansible.\n"
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "answer the question. If the answer is not in the context, "
            "say 'I don't have enough information to answer this question.'\n"
            "When appropriate, include working code examples in Python or Ansible.\n"
            "Question: {query_str}\n"
            "Answer: "
        )
        qa_template = PromptTemplate(qa_template_str)

        # Create response synthesizer
        self.response_synthesizer = CompactAndRefine(
            llm=self.llm,
            verbose=config.VERBOSE,
            text_qa_template=qa_template
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
