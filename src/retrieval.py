"""
Banking AI - FAISS Retriever

Loads the FAISS vector store and performs semantic similarity
search against the banking knowledge base.

Each result includes:
- similarity score
- content
- source
- section
"""

import json
from pathlib import Path

import faiss
import numpy as np

from embeddings import LocalEmbeddings


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = PROJECT_ROOT / "data" / "faiss_index"

INDEX_FILE = INDEX_DIR / "banking.index"
CHUNKS_FILE = INDEX_DIR / "chunks.json"


# ============================================================
# Banking Retriever
# ============================================================

class BankingRetriever:

    def __init__(self, top_k=3):

        self.top_k = top_k

        # ----------------------------------------------------
        # Load FAISS index
        # ----------------------------------------------------

        print(
            "[Retriever] Loading FAISS index..."
        )

        if not INDEX_FILE.exists():

            raise FileNotFoundError(
                f"FAISS index not found: "
                f"{INDEX_FILE}"
            )

        self.index = faiss.read_index(
            str(INDEX_FILE)
        )

        print(
            f"[Retriever] FAISS index loaded. "
            f"Vectors: {self.index.ntotal}"
        )

        # ----------------------------------------------------
        # Load chunk metadata
        # ----------------------------------------------------

        print(
            "[Retriever] Loading chunk data..."
        )

        if not CHUNKS_FILE.exists():

            raise FileNotFoundError(
                f"Chunk file not found: "
                f"{CHUNKS_FILE}"
            )

        with open(
            CHUNKS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            self.chunks = json.load(file)

        print(
            f"[Retriever] Loaded "
            f"{len(self.chunks)} chunks."
        )

        # ----------------------------------------------------
        # Load embedding model
        # ----------------------------------------------------

        self.embedding_model = LocalEmbeddings()

    # ========================================================
    # Search
    # ========================================================

    def search(self, query):

        # ----------------------------------------------------
        # Convert query to embedding
        # ----------------------------------------------------

        query_embedding = np.array(
            self.embedding_model.embed_query(query),
            dtype="float32"
        ).reshape(1, -1)

        # ----------------------------------------------------
        # Search FAISS
        # ----------------------------------------------------

        scores, indices = self.index.search(
            query_embedding,
            self.top_k
        )

        results = []

        # ----------------------------------------------------
        # Build retrieval results
        # ----------------------------------------------------

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            # FAISS can return -1 when no result exists
            if index < 0:
                continue

            chunk = self.chunks[index]

            metadata = chunk.get(
                "metadata",
                {}
            )

            results.append(
                {
                    "score": float(score),

                    "content": chunk.get(
                        "content",
                        ""
                    ),

                    "metadata": metadata,

                    # Convenient direct access
                    "section": metadata.get(
                        "section",
                        ""
                    ),

                    "source": metadata.get(
                        "source",
                        ""
                    ),
                }
            )

        return results


# ============================================================
# Test Retriever
# ============================================================

def main():

    print("=" * 70)
    print("BANKING AI - RETRIEVER TEST")
    print("=" * 70)

    retriever = BankingRetriever(
        top_k=3
    )

    test_queries = [

        "What should I do if my debit card was stolen?",

        "What should I do about an unrecognized transaction?",

        "Can the chatbot transfer money for me?",

        "Can you give me legal advice about a bank dispute?",
    ]

    for query in test_queries:

        print()
        print("-" * 70)
        print(f"Query: {query}")
        print("-" * 70)

        results = retriever.search(
            query
        )

        for rank, result in enumerate(
            results,
            start=1
        ):

            print(
                f"{rank}. "
                f"{result['section']} "
                f"(score={result['score']:.4f})"
            )

            print(
                f"   Source: "
                f"{result['source']}"
            )

            preview = (
                result["content"]
                .replace("\n", " ")
            )

            print(
                f"   Content: "
                f"{preview[:180]}..."
            )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    main()