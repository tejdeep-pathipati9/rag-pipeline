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


@pytest.fixture
def corpus(tmp_path):
    """Create one source alongside non-corpus material that must never be indexed."""
    root = tmp_path / "corpus"
    root.mkdir()
    (tmp_path / "evaluation.md").write_text("Never index this evaluation label.")
    (root / "policy.md").write_text(
        "---\ndocument_id: TEST-POLICY\ndocument_type: policy\ntitle: Hotel Policy\n"
        'version: "2.0"\neffective_from: 2026-01-01\nstatus: current\n---\n'
        "# Hotel Policy\n\n## 1. Eligibility\nHotel eligible.\n\n"
        "### 1.1 Exceptions\nHotel excluded.\n\n## 2. Refunds\nRefund reviewed.\n"
    )
    return root
