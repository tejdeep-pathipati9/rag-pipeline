"""Tests for token-bounded chunks that prefer paragraph and line boundaries.

The convenience function and configured chunker objects share the same behavior.
Chunk size and overlap are token counts. The word tokenizer below is only a
predictable test substitute; the pipeline will use its embedding model's tokenizer.
"""

import re

import pytest

from src.chunking.base import BaseChunker
from src.chunking.recursive import RecursiveChunker, chunk_text


class WordTokenizer:
    """Treat each whitespace-separated word as one token for these offline tests."""

    def encode(self, text):
        """Return word tokens that are easy to count by hand."""
        return text.split()

    def decode(self, tokens):
        """Turn the test tokens back into readable text."""
        return " ".join(tokens)

    def encode_with_offsets(self, text):
        """Expose source positions using the same whitespace rule as encode()."""
        matches = list(re.finditer(r"\S+", text))
        return [match.group() for match in matches], [match.span() for match in matches]


@pytest.fixture
def tokenizer():
    """Supply a tokenizer without downloading a model or calling an API."""
    return WordTokenizer()


@pytest.mark.parametrize("text", ["", "   \n\t"])
def test_empty_text_returns_no_chunks(tokenizer, text):
    """Empty or whitespace-only input should not produce searchable chunks."""
    assert chunk_text(text, tokenizer=tokenizer, chunk_size=4, overlap=0) == []


def test_short_text_stays_in_one_chunk(tokenizer):
    """Text that fits the budget should be returned without changes."""
    text = "A hotel may be provided."

    assert chunk_text(text, tokenizer=tokenizer, chunk_size=8, overlap=0) == [text]


def test_long_text_respects_token_limit_without_losing_words(tokenizer):
    """A paragraph exceeding the limit must split into bounded, ordered chunks."""
    text = "one two three four five six seven"

    chunks = chunk_text(text, tokenizer=tokenizer, chunk_size=3, overlap=0)

    assert chunks == ["one two three", "four five six", "seven"]
    assert all(len(tokenizer.encode(chunk)) <= 3 for chunk in chunks)
    assert " ".join(chunks) == text


def test_exact_multiple_does_not_add_an_empty_chunk(tokenizer):
    """A full final batch should be emitted once, without an empty tail."""
    chunks = chunk_text("one two three four five six", tokenizer=tokenizer, chunk_size=3, overlap=0)

    assert chunks == ["one two three", "four five six"]


def test_overlap_repeats_context_without_an_extra_tail_chunk(tokenizer):
    """Repeat two tokens between chunks, stopping once the full input is covered."""
    text = "one two three four five six seven eight"

    chunks = chunk_text(text, tokenizer=tokenizer, chunk_size=4, overlap=2)

    assert chunks == [
        "one two three four",
        "three four five six",
        "five six seven eight",
    ]


@pytest.mark.parametrize(
    ("text", "chunk_size", "overlap", "expected"),
    [
        (
            "one two three four five six seven",
            4,
            2,
            ["one two three four", "three four five six", "five six seven"],
        ),
        (
            "one two three four five",
            3,
            2,
            ["one two three", "two three four", "three four five"],
        ),
    ],
)
def test_overlap_handles_partial_tails_and_one_token_steps(
    tokenizer, text, chunk_size, overlap, expected
):
    """Keep new tail tokens and make progress even with the largest valid overlap."""
    assert chunk_text(text, tokenizer=tokenizer, chunk_size=chunk_size, overlap=overlap) == expected


@pytest.mark.parametrize(("chunk_size", "overlap"), [(0, 0), (-1, 0), (4, -1), (4, 4), (4, 5)])
def test_invalid_chunk_settings_raise_value_error(tokenizer, chunk_size, overlap):
    """Require a positive chunk size and overlap that leaves room for new tokens."""
    with pytest.raises(ValueError):
        chunk_text("one", tokenizer=tokenizer, chunk_size=chunk_size, overlap=overlap)


def test_paragraph_boundary_is_preferred_when_paragraphs_fit(tokenizer):
    """Keep complete paragraphs together before falling back to smaller splits."""
    first = "Paragraph one explains eligibility."
    second = "Paragraph two lists exclusions."

    chunks = chunk_text(first + "\n\n" + second, tokenizer=tokenizer, chunk_size=6, overlap=0)

    assert chunks == [first, second]


def test_paragraphs_that_fit_together_share_a_chunk(tokenizer):
    """Pack small paragraphs together before starting another chunk."""
    text = "one two\n\nthree four\n\nfive six"

    assert chunk_text(text, tokenizer=tokenizer, chunk_size=4, overlap=0) == [
        "one two\n\nthree four",
        "five six",
    ]


def test_overlap_spans_a_paragraph_boundary(tokenizer):
    """Retain context from the previous paragraph when the next chunk has room."""
    text = "one two three four\n\nfive six seven eight"

    assert chunk_text(text, tokenizer=tokenizer, chunk_size=6, overlap=2) == [
        "one two three four",
        "three four\n\nfive six seven eight",
    ]


def test_long_paragraph_falls_back_to_line_boundaries(tokenizer):
    """Preserve complete lines when no paragraph boundary fits the budget."""
    text = "one two three four\nfive six seven eight"

    assert chunk_text(text, tokenizer=tokenizer, chunk_size=6, overlap=0) == [
        "one two three four",
        "five six seven eight",
    ]


def test_split_chunks_keep_original_casing_and_internal_spacing(tokenizer):
    """Token counting should not rewrite the source text."""
    text = "Hotel   Eligibility\nMeals\n\nRefund   Choices Available"

    assert chunk_text(text, tokenizer=tokenizer, chunk_size=4, overlap=0) == [
        "Hotel   Eligibility\nMeals",
        "Refund   Choices Available",
    ]


def test_base_chunker_requires_a_strategy(tokenizer):
    """The base supplies shared behavior but requires a concrete boundary rule."""
    with pytest.raises(TypeError, match="abstract"):
        BaseChunker(tokenizer=tokenizer, chunk_size=4, overlap=0)


def test_recursive_chunker_can_be_configured_once_and_reused(tokenizer):
    """A strategy object keeps configuration while accepting different source texts."""
    chunker = RecursiveChunker(tokenizer=tokenizer, chunk_size=4, overlap=2)

    assert chunker.chunk_text("one two three four five six") == [
        "one two three four",
        "three four five six",
    ]
    assert chunker.chunk_text("A short passage.") == ["A short passage."]


def test_another_boundary_rule_reuses_shared_overlap_and_source_slicing(tokenizer):
    """A subclass changes only boundary selection, leaving the shared loop intact."""

    class TokenBoundaryChunker(BaseChunker):
        """Test strategy that fills the token budget regardless of paragraph breaks."""

        def _choose_split_position(self, text, max_split_position):
            """Use the full token-bounded window supplied by the base class."""
            return max_split_position

    chunker = TokenBoundaryChunker(tokenizer=tokenizer, chunk_size=4, overlap=2)

    assert chunker.chunk_text("one two\n\nthree four five six") == [
        "one two\n\nthree four",
        "three four five six",
    ]


def test_invalid_strategy_boundary_is_rejected(tokenizer):
    """A strategy must advance through the input without exceeding the safe boundary."""

    class InvalidBoundaryChunker(BaseChunker):
        """Test strategy that incorrectly asks to split after the token limit."""

        def _choose_split_position(self, text, max_split_position):
            """Return an invalid boundary to exercise the shared contract check."""
            return max_split_position + 1

    chunker = InvalidBoundaryChunker(tokenizer=tokenizer, chunk_size=2, overlap=0)

    with pytest.raises(ValueError, match="split position"):
        chunker.chunk_text("one two three")
