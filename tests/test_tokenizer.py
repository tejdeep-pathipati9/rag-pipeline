"""Exercise real subword tokenization using a tiny local vocabulary, without downloads."""

import pytest
from transformers import BertTokenizer

from src.tokenizer import ModelTokenizer


@pytest.fixture
def tokenizer(tmp_path):
    """Save a real tokenizer locally so tests use the same loader as a pretrained model."""
    vocabulary = [
        "[PAD]",
        "[UNK]",
        "[CLS]",
        "[SEP]",
        "[MASK]",
        "north",
        "##star",
        "re",
        "##book",
        "##ed",
        "my",
        "flight",
        ".",
    ]
    backend = BertTokenizer(
        vocab={token: index for index, token in enumerate(vocabulary)},
        do_lower_case=True,
        model_max_length=8,
    )
    backend.save_pretrained(tmp_path)
    return ModelTokenizer(str(tmp_path))


def test_encode_returns_subword_ids_without_added_special_tokens(tokenizer):
    """Count actual word pieces and punctuation rather than whitespace-separated words."""
    assert tokenizer.encode("Northstar rebooked my flight.") == [5, 6, 7, 8, 9, 10, 11, 12]


def test_long_input_is_not_silently_truncated(tokenizer):
    """The chunker needs the complete token count even when input exceeds the model limit."""
    assert tokenizer.encode("flight " * 20) == [11] * 20


def test_decode_joins_subwords_using_the_model_rules(tokenizer):
    """Decoding reconstructs readable text, including the model's lowercase normalization."""
    assert tokenizer.decode([5, 6, 7, 8, 9, 10, 11, 12]) == "northstar rebooked my flight."


def test_empty_input_has_no_content_tokens(tokenizer):
    """Empty input should not acquire model boundary tokens."""
    assert tokenizer.encode("") == []
    assert tokenizer.decode([]) == ""
