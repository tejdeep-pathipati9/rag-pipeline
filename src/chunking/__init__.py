"""Chunking strategies that inherit a shared workflow from BaseChunker.

Choose a concrete strategy, configure it once, then pass source text to it:

    chunker = RecursiveChunker(tokenizer=tokenizer, chunk_size=128, overlap=16)
    chunks = chunker.chunk_text(text)

BaseChunker handles validation, token limits, source slicing and overlap.
Subclasses implement only their boundary-selection rule. This shared workflow
is the Template Method pattern; choosing a concrete chunker uses the Strategy
pattern. Tokenizer loading, embeddings and vector storage belong elsewhere.

The existing chunk_text() function remains a convenience for the baseline.
"""

from .base import BaseChunker
from .recursive import RecursiveChunker, chunk_text

__all__ = ["BaseChunker", "RecursiveChunker", "chunk_text"]
