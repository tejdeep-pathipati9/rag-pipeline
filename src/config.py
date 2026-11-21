"""Application settings and chunking selection."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

from src.chunking import MarkdownChunker, ParentChildChunker, RecursiveChunker
from src.embedding import DEFAULT_MODEL, DEFAULT_REVISION

CHUNKING_STRATEGIES = {
    "recursive": RecursiveChunker,
    "markdown": MarkdownChunker,
    "parent-child": ParentChildChunker,
}


@dataclass
class AppConfig:
    """Keep defaults and environment settings together; loading creates no clients."""

    namespace: str = "policy-qa-parent-child-200-40-v1"
    batch_size: int = 64
    retrieval_k: int = 20
    embedding_model: str = DEFAULT_MODEL
    embedding_revision: str = DEFAULT_REVISION
    cache_dir: str = ".cache/models"
    pinecone_index_name: str = ""
    pinecone_api_key: str = field(default="", repr=False)
    llm_model: str = ""
    llm_base_url: str = ""
    llm_api_key: str = field(default="", repr=False)

    @classmethod
    def from_env(cls):
        """Read local settings while preserving existing environment overrides."""
        load_dotenv(".env")
        return cls(
            embedding_model=os.getenv("EMBEDDING_MODEL", cls.embedding_model),
            embedding_revision=os.getenv("EMBEDDING_REVISION", cls.embedding_revision),
            cache_dir=os.getenv("MODEL_CACHE_DIR", cls.cache_dir),
            pinecone_index_name=os.getenv("PINECONE_INDEX_NAME", ""),
            pinecone_api_key=os.getenv("PINECONE_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", ""),
            llm_base_url=os.getenv("LLM_BASE_URL", ""),
            llm_api_key=os.getenv("LLM_API_KEY", ""),
        )

    def validate(self, *, require_index: bool, require_llm: bool):
        """Require only the services used by the selected operation."""
        required = {}
        if require_index:
            required.update(
                PINECONE_API_KEY=self.pinecone_api_key, PINECONE_INDEX_NAME=self.pinecone_index_name
            )
        if require_llm:
            required.update(
                LLM_API_KEY=self.llm_api_key,
                LLM_MODEL=self.llm_model,
                LLM_BASE_URL=self.llm_base_url,
            )
        missing = [name for name, value in required.items() if not value.strip()]
        if missing:
            raise ValueError(f"Set {', '.join(missing)} in your local .env.")


@dataclass
class ChunkingConfig:
    """Choose the default strategy, chunk size and overlap here."""

    strategy: str = "parent-child"
    chunk_size: int = 200
    overlap: int = 40

    def create_chunker(self, tokenizer):
        """Build the selected chunker with these settings."""
        if self.strategy not in CHUNKING_STRATEGIES:
            raise ValueError(f"Unknown chunking strategy: {self.strategy}")
        return CHUNKING_STRATEGIES[self.strategy](tokenizer, self.chunk_size, self.overlap)
