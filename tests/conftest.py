"""Shared, predictable tokenizer for offline chunking and ingestion tests."""

import re

import pytest


class WordTokenizer:
    """Treat each whitespace-separated word as one token."""

    def encode(self, text):
        """Return words so token counts can be checked by hand."""
        return text.split()

    def encode_with_offsets(self, text):
        """Return words and their positions in the unchanged source text."""
        matches = list(re.finditer(r"\S+", text))
        return [match.group() for match in matches], [match.span() for match in matches]


@pytest.fixture
def tokenizer():
    """Provide token counting without a model download or API request."""
    return WordTokenizer()
