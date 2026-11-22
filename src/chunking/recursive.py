"""Baseline strategy: prefer paragraphs, then lines, then token boundaries."""

import re

from .base import BaseChunker

# A paragraph break is a blank line, which may contain spaces or Windows line endings.
PARAGRAPH_BREAK = re.compile(r"\r?\n[ \t\r]*\n")
LINE_BREAK = re.compile(r"\r?\n")


class RecursiveChunker(BaseChunker):
    """Prefer paragraph breaks, then line breaks, then the token limit.

    BaseChunker supplies configuration, chunk creation and overlap. This class
    implements only the boundary rule specific to the baseline strategy.
    """

    strategy = "recursive"

    def _choose_split_position(self, text: str, max_split_position: int) -> int:
        """Prefer the last safe paragraph break, then the last safe line break.

        Search paragraph boundaries first even if a line break occurs later.
        If neither exists, return the supplied safe character limit so the base
        class can split at the token boundary. Never select the start of text.
        """
        for break_pattern in (PARAGRAPH_BREAK, LINE_BREAK):
            last_break_position = None

            for match in break_pattern.finditer(text):
                break_position = match.start()
                if break_position > 0 and break_position <= max_split_position:
                    last_break_position = break_position

            if last_break_position is not None:
                return last_break_position

        return max_split_position


def chunk_text(text: str, tokenizer, chunk_size: int, overlap: int) -> list[str]:
    """Split text with recursive boundaries and return the resulting source strings.

    Convenience wrapper around RecursiveChunker. chunk_size and overlap are
    token counts measured by the supplied model tokenizer, not word counts.
    """
    chunker = RecursiveChunker(tokenizer=tokenizer, chunk_size=chunk_size, overlap=overlap)
    return chunker.chunk_text(text)
