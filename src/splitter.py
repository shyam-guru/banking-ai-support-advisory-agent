"""
Split the banking knowledge base into section-aware chunks.

Each chunk retains the section name in its metadata so that
retrieval results can identify the originating knowledge-base
section even when a section is split across multiple chunks.
"""

import re

from langchain_text_splitters import RecursiveCharacterTextSplitter

from loader import load_knowledge_base


# ============================================================
# Configuration
# ============================================================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100


# ============================================================
# Helper Function
# ============================================================

def clean_section_name(heading):
    """
    Convert a Markdown section heading into a clean section name.

    Examples:

        # 1. Lost or Stolen Debit Card
        -> Lost or Stolen Debit Card

        ## 8. Legal Advice
        -> Legal Advice
    """

    # Remove Markdown heading markers
    heading = re.sub(r"^#+\s*", "", heading).strip()

    # Remove section number such as 1., 2., 10.
    heading = re.sub(r"^\d+\.\s*", "", heading)

    return heading.strip()


def get_section_name(text):
    """
    Find the most recent Markdown heading in a block of text.

    Returns an empty string if no heading is found.
    """

    for line in text.splitlines():

        line = line.strip()

        if line.startswith("#"):

            return clean_section_name(line)

    return ""


# ============================================================
# Split Documents
# ============================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n# ",
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            " ",
        ],
    )

    chunks = splitter.split_documents(documents)

    # --------------------------------------------------------
    # Add section metadata
    # --------------------------------------------------------

    current_section = ""

    for chunk in chunks:

        section_name = get_section_name(
            chunk.page_content
        )

        # If this chunk contains a heading, update
        # the current section.
        if section_name:
            current_section = section_name

        # If the chunk does not contain a heading,
        # inherit the section from the previous chunk.
        chunk.metadata["section"] = current_section

    return chunks


# ============================================================
# Test / Preview
# ============================================================

def main():

    print("=" * 70)
    print("BANKING AI - DOCUMENT SPLITTER")
    print("=" * 70)

    print()
    print("[Splitter] Loading documents...")

    documents = load_knowledge_base()

    print()
    print("[Splitter] Splitting documents...")

    chunks = split_documents(documents)

    print(
        f"[Splitter] Created {len(chunks)} chunks "
        f"from {len(documents)} document(s)"
    )

    print()

    # --------------------------------------------------------
    # Preview first 10 chunks
    # --------------------------------------------------------

    for i, chunk in enumerate(chunks[:10], start=1):

        print("-" * 70)

        print(f"Chunk {i}")
        print(
            f"Section: "
            f"{chunk.metadata.get('section', '')}"
        )

        print(
            f"Source: "
            f"{chunk.metadata.get('source', '')}"
        )

        preview = chunk.page_content[:300]

        print("Content:")
        print(preview)

        if len(chunk.page_content) > 300:
            print("...")

    print("-" * 70)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()