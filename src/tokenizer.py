"""Turn source text into model tokens and locate those tokens in the original text."""

from transformers import AutoTokenizer


class ModelTokenizer:
    """Load a model's vocabulary and rules for splitting text into tokens.

    model_name can be a Hugging Face model ID or a local tokenizer directory.
    revision optionally selects a specific version of the tokenizer files.
    Loading a tokenizer does not load the embedding model's weights.
    """

    def __init__(self, model_name: str, *, revision: str | None = None):
        """Load the tokenizer files from the local cache, a directory, or Hugging Face."""
        self._tokenizer = AutoTokenizer.from_pretrained(model_name, revision=revision)

    def encode(self, text: str) -> list[int]:
        """Return token IDs so len(token_ids) gives the text's content token count.

        Exclude special tokens such as [CLS] and [SEP]. Keep the entire input,
        even when it is too long for the model, so the chunker can split it.
        """
        return self._tokenizer.encode(
            text,
            add_special_tokens=False,
            truncation=False,
        )

    def decode(self, token_ids: list[int]) -> str:
        """Convert token IDs back into readable text.

        A tokenizer may lowercase text or change spacing. The chunker uses the
        original text and token positions instead of decode() to preserve it.
        """
        return self._tokenizer.decode(token_ids, clean_up_tokenization_spaces=False)

    def encode_with_offsets(self, text: str) -> tuple[list[int], list[tuple[int, int]]]:
        """Return token IDs together with each token's (start, end) character position.

        For example, a token covering "Hotel" in "Hotel stay" has position (0, 5).
        text[0:5] retrieves "Hotel" directly from the original source. Hugging Face
        calls these positions "offsets" and returns them as "offset_mapping".
        """
        tokenized_text = self._tokenizer(
            text,
            add_special_tokens=False,
            truncation=False,
            return_offsets_mapping=True,
        )
        token_ids = tokenized_text["input_ids"]
        token_positions = tokenized_text["offset_mapping"]
        return token_ids, token_positions
