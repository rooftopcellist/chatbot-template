"""
Embedding engine module for creating and managing embeddings.
"""

import os
import pickle
from typing import List
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document
import config

class EmbeddingEngine:
    """
    Handles document chunking, embedding, and vector storage.
    """

    def __init__(self):
        """Initialize the embedding engine."""
        # Create embedding model
        self.embed_model = HuggingFaceEmbedding(
            model_name=config.EMBEDDING_MODEL_NAME
        )

        # Create node parser for chunking
        self.node_parser = SentenceSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP
        )

        # Initialize vector store and index
        self.vector_store = None
        self.index = None

        # Ensure persistence directory exists
        os.makedirs(config.INDEX_PERSIST_DIR, exist_ok=True)

    def load_or_create_index(self, documents: List[Document]) -> VectorStoreIndex:
        """
        Load an existing index or create a new one if it doesn't exist.

        Args:
            documents (List[Document]): Documents to index if creating a new index

        Returns:
            VectorStoreIndex: The loaded or created index
        """
        # Check if index exists
        if self._index_exists():
            print("Loading existing index...")

            # Load the persisted index
            with open(os.path.join(config.INDEX_PERSIST_DIR, "index.pkl"), "rb") as f:
                self.index = pickle.load(f)

            print("Index loaded successfully")
        else:
            print("Creating new index...")
            # Process documents into nodes (chunks)
            nodes = self.node_parser.get_nodes_from_documents(documents)
            print(f"Created {len(nodes)} chunks from {len(documents)} documents")

            # Create vector store
            self.vector_store = SimpleVectorStore()
            storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

            # Create index
            self.index = VectorStoreIndex(
                nodes=nodes,
                storage_context=storage_context,
                embed_model=self.embed_model
            )

            # Persist index
            self._persist_index()

        return self.index

    def _index_exists(self) -> bool:
        """
        Check if an index exists in the persistence directory.

        Returns:
            bool: True if index exists, False otherwise
        """
        # Check for index file
        index_file = os.path.join(config.INDEX_PERSIST_DIR, "index.pkl")
        return os.path.exists(index_file)

    def _persist_index(self) -> None:
        """Persist the index to disk."""
        if self.index:
            # Create directory if it doesn't exist
            os.makedirs(config.INDEX_PERSIST_DIR, exist_ok=True)

            # Save the index
            with open(os.path.join(config.INDEX_PERSIST_DIR, "index.pkl"), "wb") as f:
                pickle.dump(self.index, f)

            print(f"Index persisted to {config.INDEX_PERSIST_DIR}")
        else:
            print("No index to persist")
