"""Create local baseline embeddings with the same tokenizer used for chunking."""

from sentence_transformers import SentenceTransformer

from src.tokenizer import ModelTokenizer

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_REVISION = "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"


class EmbeddingModel:
    """Load one Sentence Transformer and reuse it across all ingestion batches."""

    def __init__(self, model_name: str, *, revision: str, cache_dir: str = ".cache/models"):
        """Load pinned weights and tokenizer files from the same model version."""
        self.model_name = model_name
        self.revision = revision
        self._model = SentenceTransformer(
            model_name, revision=revision, cache_folder=cache_dir, device="cpu"
        )
        self.tokenizer = ModelTokenizer(model_name, revision=revision, cache_dir=cache_dir)
        self.dimension = self._model.get_embedding_dimension()

        # Chunk sizes count source tokens; model input also needs boundary tokens.
        special_tokens = self._model.tokenizer.num_special_tokens_to_add(pair=False)
        self.max_content_tokens = self._model.max_seq_length - special_tokens

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed original chunk text, rejecting input that the model would truncate."""
        if not texts:
            return []
        for text in texts:
            if len(self.tokenizer.encode(text)) > self.max_content_tokens:
                raise ValueError("Chunk exceeds the embedding model's content token limit.")

        vectors = self._model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False, prompt=""
        )
        return vectors.tolist()
