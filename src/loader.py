"""
Document loader for the Banking AI knowledge base.

This module loads approved banking knowledge documents
from the local knowledge_base directory.
"""

from pathlib import Path

from langchain_community.document_loaders import TextLoader


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Knowledge-base directory
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"


def load_knowledge_base():
    """
    Load all Markdown knowledge-base documents.

    Returns:
        List of LangChain Document objects.
    """

    documents = []

    markdown_files = list(KNOWLEDGE_BASE_DIR.glob("*.md"))

    if not markdown_files:
        raise FileNotFoundError(
            f"No Markdown files found in {KNOWLEDGE_BASE_DIR}"
        )

    for file_path in markdown_files:

        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
        )

        loaded_documents = loader.load()

        documents.extend(loaded_documents)

        print(
            f"[Loader] Loaded {file_path.name} "
            f"({len(loaded_documents)} document(s))"
        )

    print(
        f"[Loader] Total documents loaded: {len(documents)}"
    )

    return documents


if __name__ == "__main__":

    docs = load_knowledge_base()

    print("\n--- First Document Preview ---")

    print(docs[0].page_content[:500])

    print("\nMetadata:")
    print(docs[0].metadata)