"""Create local baseline embeddings with the same tokenizer used for chunking."""

from sentence_transformers import SentenceTransformer

from src.tokenizer import ModelTokenizer

DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# Pin the weights and tokenizer files so later downloads do not silently change a run.
DEFAULT_REVISION = "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"


class EmbeddingModel:
    """Embed source bodies and questions with one shared Sentence Transformer.

    Expose its tokenizer, vector dimension and usable content-token limit so
    chunking, ingestion and retrieval use the same model constraints.
    """

    def __init__(self, model_name: str, *, revision: str, cache_dir: str = ".cache/models"):
        """Load the specified model revision and matching tokenizer on the CPU.

        Reuse cached files when available; loading may download missing files.
        Derive vector dimension and content capacity from the model itself,
        reserving space for its special tokens. Raise ValueError if the model
        does not report a positive embedding dimension.
        """
        self.model_name = model_name
        self.revision = revision
        self._model = SentenceTransformer(
            model_name, revision=revision, cache_folder=cache_dir, device="cpu"
        )
        self.tokenizer = ModelTokenizer(model_name, revision=revision, cache_dir=cache_dir)
        # Every vector has this many values: 384 for our MiniLM baseline.
        # Pinecone's dense field must use the same dimension.
        dimension = self._model.get_embedding_dimension()
        if dimension is None or dimension <= 0:
            raise ValueError("Embedding model must report a positive vector dimension.")
        self.dimension: int = dimension

        # Chunk sizes count source tokens; model input also needs boundary tokens.
        # MiniLM allows 256 positions: two special tokens leave 254 for content.
        special_tokens = self._model.tokenizer.num_special_tokens_to_add(pair=False)
        self.max_content_tokens = self._model.max_seq_length - special_tokens

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return normalized vectors in input order, or [] for an empty list.

        Use original chunk text for ingestion and the question text for retrieval.
        Vectors are ordinary Python lists with self.dimension values each;
        metadata is stored separately and never concatenated with these texts.
        Raise ValueError if any input exceeds the model's content-token capacity,
        before the embedding library can silently truncate a policy condition.
        """
        if not texts:
            return []
        for text in texts:
            if len(self.tokenizer.encode(text)) > self.max_content_tokens:
                raise ValueError("Text exceeds the embedding model's content token limit.")

        # Produce unit-length vectors. An empty prompt prevents a saved model
        # prompt from adding a prefix to the supplied chunk text.
        vectors = self._model.encode(
            texts, normalize_embeddings=True, show_progress_bar=False, prompt=""
        )
        # Pinecone accepts ordinary Python lists, rather than NumPy arrays.
        return vectors.tolist()
