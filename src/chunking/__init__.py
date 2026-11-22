"""Chunking strategies that inherit a shared workflow from BaseChunker.

Choose a concrete strategy, configure it once, then pass source text to it:

    chunker = RecursiveChunker(tokenizer=tokenizer, chunk_size=128, overlap=16)
    chunks = chunker.chunk_text(text)

BaseChunker handles validation, token limits, source slicing and overlap.
RecursiveChunker selects paragraph and line boundaries. MarkdownChunker packs
complete sections and blocks, using the recursive fallback for oversized units.
ParentChildChunker bounds children within level-two sections and retains parent
positions so retrieval can recover the full source context after ranking.
Tokenizer loading, embeddings and vector storage belong elsewhere.

The existing chunk_text() function remains a convenience for the baseline.
"""

from .base import BaseChunker
from .markdown import MarkdownChunker
from .parent_child import ParentChildChunker
from .recursive import RecursiveChunker, chunk_text

__all__ = ["BaseChunker", "MarkdownChunker", "ParentChildChunker", "RecursiveChunker", "chunk_text"]
