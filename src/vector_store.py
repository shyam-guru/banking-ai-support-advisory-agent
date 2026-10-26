"""
Build and save the FAISS vector store for the banking knowledge base.

Each stored chunk includes:
- content
- source
- section

The section metadata allows the retriever and evaluator to identify
the originating knowledge-base section even when a section contains
multiple chunks.
"""

import json
from pathlib import Path

import faiss
import numpy as np

from embeddings import LocalEmbeddings
from splitter import split_documents
from loader import load_knowledge_base


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = PROJECT_ROOT / "data" / "faiss_index"

INDEX_FILE = INDEX_DIR / "banking.index"

CHUNKS_FILE = INDEX_DIR / "chunks.json"


# ============================================================
# Build Vector Store
# ============================================================

def build_vector_store():

    print()
    print("[Vector Store] Loading knowledge base...")

    documents = load_knowledge_base()

    print()
    print("[Vector Store] Splitting documents...")

    chunks = split_documents(documents)

    print(
        f"[Vector Store] Created {len(chunks)} chunks."
    )

    # --------------------------------------------------------
    # Load embedding model
    # --------------------------------------------------------

    print()
    print(
        f"[Vector Store] Embedding {len(chunks)} chunks..."
    )

    embedding_model = LocalEmbeddings()

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = embedding_model.embed_documents(
        texts
    )

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    # --------------------------------------------------------
    # Create FAISS index
    # --------------------------------------------------------

    dimension = embeddings.shape[1]

    print(
        f"[Vector Store] Embedding dimension: {dimension}"
    )

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print(
        f"[Vector Store] FAISS index contains "
        f"{index.ntotal} vectors."
    )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Save FAISS index
    # --------------------------------------------------------

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    print(
        "[Vector Store] Index saved to:"
    )

    print(
        INDEX_FILE.resolve()
    )

    # --------------------------------------------------------
    # Save chunk metadata
    # --------------------------------------------------------

    chunk_data = []

    for chunk in chunks:

        chunk_data.append(
            {
                "content": chunk.page_content,

                "metadata": {
                    "source": chunk.metadata.get(
                        "source",
                        ""
                    ),

                    "section": chunk.metadata.get(
                        "section",
                        ""
                    ),
                },
            }
        )

    with open(
        CHUNKS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunk_data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        "[Vector Store] Chunk metadata saved to:"
    )

    print(
        CHUNKS_FILE.resolve()
    )

    # --------------------------------------------------------
    # Print section summary
    # --------------------------------------------------------

    print()
    print("[Vector Store] Section metadata summary:")

    for i, chunk in enumerate(
        chunk_data,
        start=1
    ):

        section = chunk["metadata"]["section"]

        print(
            f"  Chunk {i}: {section}"
        )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("BANKING AI - FAISS VECTOR STORE")
    print("=" * 70)

    build_vector_store()