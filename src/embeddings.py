"""
Local embedding model for the Banking AI RAG system.

This is a temporary development implementation.

The final project can replace this local embedding model
with OpenAI Embeddings once API access is available.
"""

from sentence_transformers import SentenceTransformer


# Small and efficient local embedding model.
# It is suitable for a small capstone knowledge base.
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


class LocalEmbeddings:
    """
    Wrapper around Sentence Transformers.

    Provides methods compatible with the operations we need
    for document and query embeddings.
    """

    def __init__(self):
        print(
            f"[Embeddings] Loading model: "
            f"{EMBEDDING_MODEL_NAME}"
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL_NAME
        )

        print("[Embeddings] Model loaded successfully.")

    def embed_documents(self, texts):
        """
        Convert multiple documents into vectors.

        Args:
            texts: List of strings.

        Returns:
            List of embedding vectors.
        """

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()

    def embed_query(self, text):
        """
        Convert a user query into a vector.

        Args:
            text: Query string.

        Returns:
            Query embedding vector.
        """

        embedding = self.model.encode(
            [text],
            normalize_embeddings=True,
        )[0]

        return embedding.tolist()


if __name__ == "__main__":

    embedding_model = LocalEmbeddings()

    test_text = (
        "What should I do if my debit card is stolen?"
    )

    vector = embedding_model.embed_query(test_text)

    print("\nEmbedding test:")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")