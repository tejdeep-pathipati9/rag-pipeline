"""First tests for the recursive text chunker; implementation comes next.

Expected API: chunk_text(text, tokenizer=..., chunk_size=..., overlap=...) -> list[str].
Chunk size and overlap are token counts. The word tokenizer below is only a
predictable test substitute; the pipeline will use its embedding model's tokenizer.
"""

import pytest

from src.chunking import chunk_text


class WordTokenizer:
    """Treat each whitespace-separated word as one token for these offline tests."""

    def encode(self, text):
        """Return word tokens that are easy to count by hand."""
        return text.split()

    def decode(self, tokens):
        """Turn the test tokens back into readable text."""
        return " ".join(tokens)


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


def test_overlap_repeats_context_without_an_extra_tail_chunk(tokenizer):
    """Repeat two tokens between chunks, stopping once the full input is covered."""
    text = "one two three four five six seven eight"

    chunks = chunk_text(text, tokenizer=tokenizer, chunk_size=4, overlap=2)

    assert chunks == [
        "one two three four",
        "three four five six",
        "five six seven eight",
    ]


def test_paragraph_boundary_is_preferred_when_paragraphs_fit(tokenizer):
    """Keep complete paragraphs together before falling back to smaller splits."""
    first = "Paragraph one explains eligibility."
    second = "Paragraph two lists exclusions."

    chunks = chunk_text(first + "\n\n" + second, tokenizer=tokenizer, chunk_size=6, overlap=0)

    assert chunks == [first, second]
