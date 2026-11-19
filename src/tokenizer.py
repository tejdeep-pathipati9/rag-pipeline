"""Load a Hugging Face model's tokenizer for measuring chunk content in tokens."""

from transformers import AutoTokenizer


class ModelTokenizer:
    """Expose token IDs and decoding without loading embedding model weights.

    Supply a model ID or a local tokenizer directory. For reproducible remote
    loads, pass the model's commit hash as ``revision``. Token counts exclude
    added special tokens; reserve space for those when setting chunk budgets.
    """

    def __init__(self, model_name: str, *, revision: str | None = None):
        """Load the supplied model's vocabulary and tokenization rules."""
        self._tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)

    def encode(self, text: str) -> list[int]:
        """Return every content token ID, without truncation or added boundary tokens."""
        return self._tokenizer.encode(text, add_special_tokens=False, truncation=False)

    def decode(self, token_ids: list[int]) -> str:
        """Decode IDs into readable text; normalization may differ from the source.

        Keep the original corpus text separately for faithful chunks and citations.
        """
        return self._tokenizer.decode(token_ids, clean_up_tokenization_spaces=False)
