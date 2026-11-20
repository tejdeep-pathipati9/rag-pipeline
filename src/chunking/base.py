"""Shared chunking workflow; subclasses decide where each chunk should end."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    """Original text and its character range in the input passed to the chunker."""

    text: str
    start: int
    end: int


class BaseChunker(ABC):
    """Handle token limits, source text and overlap for all boundary strategies.

    Configure a concrete subclass once, then call chunk_text(text) for each
    source. Subclasses implement _choose_split_position() to select boundaries
    within the safe token limit supplied by this base class.
    """

    def __init__(self, tokenizer, chunk_size: int, overlap: int):
        """Store the shared tokenizer and validate sizes, which are token counts."""
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")
        if not 0 <= overlap < chunk_size:
            raise ValueError("overlap must be nonnegative and smaller than chunk_size.")

        self.tokenizer = tokenizer
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> list[str]:
        """Return just the text when callers do not need citation positions."""
        return [chunk.text for chunk in self.chunk_with_offsets(text)]

    def chunk_with_offsets(self, text: str) -> list[TextChunk]:
        """Create token-bounded chunks together with their original source positions.

        Copy source text directly to preserve casing and internal whitespace.
        Whitespace at split boundaries is removed; short input is unchanged.
        Repeat the requested overlap when possible while always moving forward.
        """
        if not text.strip():
            return []

        token_ids = self.tokenizer.encode(text)
        if len(token_ids) <= self.chunk_size:
            return [TextChunk(text, 0, len(text))]

        chunks = []
        remaining_text = text.strip()
        # Track source positions as we consume text, even when passages repeat.
        source_start = len(text) - len(text.lstrip())

        while remaining_text:
            token_ids, token_positions = self.tokenizer.encode_with_offsets(remaining_text)

            if len(token_ids) <= self.chunk_size:
                chunks.append(
                    TextChunk(remaining_text, source_start, source_start + len(remaining_text))
                )
                break

            chunk = self._create_chunk(remaining_text, token_positions)
            chunks.append(TextChunk(chunk, source_start, source_start + len(chunk)))

            chunk_ids, chunk_positions = self.tokenizer.encode_with_offsets(chunk)
            next_start = self._choose_overlap_start(chunk_positions, len(chunk))
            next_text = remaining_text[next_start:]
            leading_whitespace = len(next_text) - len(next_text.lstrip())
            source_start += next_start + leading_whitespace
            remaining_text = next_text.lstrip()

        return chunks

    def _create_chunk(self, text: str, token_positions: list[tuple[int, int]]) -> str:
        """Ask the strategy for a boundary, then return source text that fits."""
        last_token_end = token_positions[self.chunk_size - 1][1]
        next_token_start = token_positions[self.chunk_size][0]

        # Keep a character whole when several tokens refer to the same character.
        max_split_position = min(last_token_end, next_token_start)
        if max_split_position <= 0:
            raise ValueError("chunk_size is too small to fit the next source character.")

        # Include the gap after the last token so the strategy can see a
        # paragraph break that falls exactly at the token limit.
        text_within_limit = text[:next_token_start]
        split_position = self._choose_split_position(text_within_limit, max_split_position)
        if not 0 < split_position <= max_split_position:
            raise ValueError("The strategy's split position must be within the token limit.")

        chunk = text[:split_position].rstrip()

        # A word fragment can tokenize differently on its own. Shorten the
        # actual source slice until it fits the token budget.
        while chunk and len(self.tokenizer.encode(chunk)) > self.chunk_size:
            split_position -= 1
            chunk = text[:split_position].rstrip()

        if not chunk:
            raise ValueError("chunk_size is too small to fit the next source character.")

        return chunk

    @abstractmethod
    def _choose_split_position(self, text: str, max_split_position: int) -> int:
        """Choose a character position greater than zero and at most the supplied limit.

        This is the strategy-specific step. The base class handles the rest
        of chunk creation, including token counting and overlap.
        """
        raise NotImplementedError

    def _choose_overlap_start(
        self, token_positions: list[tuple[int, int]], split_position: int
    ) -> int:
        """Find where the next chunk starts, including context from the saved chunk."""
        # No overlap, or a chunk too short to repeat without getting stuck.
        if self.overlap == 0 or len(token_positions) <= self.overlap:
            return split_position

        token_index = len(token_positions) - self.overlap
        next_start = token_positions[token_index][0]

        # Always move forward, even when token positions share a character.
        if next_start == 0:
            return split_position

        return next_start
