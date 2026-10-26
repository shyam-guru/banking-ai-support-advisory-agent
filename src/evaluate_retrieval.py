"""
Evaluate the Banking AI Agent's FAISS retrieval performance.

Evaluation method:
- Each test case has an expected knowledge-base section.
- The retrieved chunk's SECTION HEADING is extracted.
- Matching is based only on the section heading,
  not on arbitrary text appearing inside the chunk.
- Calculates Top-1 and Top-3 retrieval accuracy.
- Saves detailed results to evidence/retrieval_evaluation.json
"""

import json
import re
from pathlib import Path

from retrieval import BankingRetriever


# ============================================================
# Configuration
# ============================================================

TOP_K = 3

OUTPUT_FILE = Path("evidence/retrieval_evaluation.json")


# ============================================================
# Retrieval Test Cases
# ============================================================

TEST_CASES = [
    {
        "id": "R01",
        "query": "What should I do if my debit card was stolen?",
        "expected_section": "Lost or Stolen Debit Card",
    },
    {
        "id": "R02",
        "query": "How can I replace my lost debit card?",
        "expected_section": "Debit Card Replacement",
    },
    {
        "id": "R03",
        "query": "What should I do about an unrecognized transaction?",
        "expected_section": "Unrecognized or Unauthorized Transactions",
    },
    {
        "id": "R04",
        "query": "What documents are required to open a savings account?",
        "expected_section": "Savings Account Opening",
    },
    {
        "id": "R05",
        "query": "Can the chatbot transfer ₹50,000 from my account?",
        "expected_section": "Money Transfers",
    },
    {
        "id": "R06",
        "query": "Can you approve my loan application?",
        "expected_section": "Loan Information",
    },
    {
        "id": "R07",
        "query": "Can you tell me my current account balance?",
        "expected_section": "Customer-Specific Information",
    },
    {
        "id": "R08",
        "query": "Can you give me legal advice about a dispute with my bank?",
        "expected_section": "Legal Advice",
    },
    {
        "id": "R09",
        "query": "What information should I never share with the chatbot?",
        "expected_section": "Authentication and Sensitive Information",
    },
    {
        "id": "R10",
        "query": "When should a banking issue be escalated?",
        "expected_section": "Escalation",
    },
]


# ============================================================
# Helper Functions
# ============================================================

def normalize_text(text):
    """
    Normalize text so that comparisons are case-insensitive
    and differences in spacing do not affect matching.
    """
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)

    return text


def extract_section_heading(content):
    """
    Extract the first Markdown heading from a retrieved chunk.

    Example:

        # 1. Lost or Stolen Debit Card

    becomes:

        Lost or Stolen Debit Card

    This prevents false matches caused by section names appearing
    somewhere in the body text.
    """

    for line in content.splitlines():

        line = line.strip()

        # Look for Markdown headings such as:
        # # Heading
        # ## Heading
        # ### Heading

        if line.startswith("#"):

            # Remove Markdown # characters
            heading = re.sub(r"^#+\s*", "", line).strip()

            # Remove section number such as:
            # 1.
            # 2.
            # 10.

            heading = re.sub(r"^\d+\.\s*", "", heading)

            return heading.strip()

    return ""


def find_expected_rank(results, expected_section):
    """
    Find the rank of the expected section in the retrieved results.

    Returns:
        1, 2, 3, ... if found
        None if not found
    """

    expected_normalized = normalize_text(expected_section)

    for rank, result in enumerate(results, start=1):

        section_heading = extract_section_heading(
            result["content"]
        )

        if normalize_text(section_heading) == expected_normalized:
            return rank

    return None


# ============================================================
# Main Evaluation
# ============================================================

def main():

    print("=" * 70)
    print("BANKING AI - RETRIEVAL EVALUATION")
    print("=" * 70)

    print()
    print(f"Top-K retrieved documents : {TOP_K}")
    print("Matching method           : Exact normalized section heading")
    print()

    # --------------------------------------------------------
    # Initialize retriever
    # --------------------------------------------------------

    retriever = BankingRetriever(top_k=TOP_K)

    # --------------------------------------------------------
    # Evaluation counters
    # --------------------------------------------------------

    top1_correct = 0
    top3_correct = 0

    detailed_results = []

    # --------------------------------------------------------
    # Run test cases
    # --------------------------------------------------------

    for test in TEST_CASES:

        test_id = test["id"]
        query = test["query"]
        expected_section = test["expected_section"]

        print("-" * 70)
        print(f"{test_id}: {query}")
        print(f"Expected section: {expected_section}")

        # ----------------------------------------------------
        # Retrieve documents
        # ----------------------------------------------------

        results = retriever.search(query)

        # ----------------------------------------------------
        # Find expected section rank
        # ----------------------------------------------------

        expected_rank = find_expected_rank(
            results,
            expected_section
        )

        top1_pass = expected_rank == 1

        top3_pass = (
            expected_rank is not None
            and expected_rank <= TOP_K
        )

        # ----------------------------------------------------
        # Update metrics
        # ----------------------------------------------------

        if top1_pass:
            top1_correct += 1

        if top3_pass:
            top3_correct += 1

        # ----------------------------------------------------
        # Display results
        # ----------------------------------------------------

        print()

        if expected_rank is not None:
            print(f"Expected section rank: {expected_rank}")
        else:
            print("Expected section rank: NOT FOUND")

        print(
            f"Top-1: {'PASS' if top1_pass else 'FAIL'}"
        )

        print(
            f"Top-{TOP_K}: {'PASS' if top3_pass else 'FAIL'}"
        )

        print()
        print("Retrieved sections:")

        retrieved_sections = []

        for rank, result in enumerate(results, start=1):

            section_heading = extract_section_heading(
                result["content"]
            )

            score = result["score"]

            print(
                f"  {rank}. "
                f"{section_heading} "
                f"(score={score:.4f})"
            )

            retrieved_sections.append(
                {
                    "rank": rank,
                    "section": section_heading,
                    "score": round(float(score), 4),
                }
            )

        # ----------------------------------------------------
        # Store detailed result
        # ----------------------------------------------------

        detailed_results.append(
            {
                "id": test_id,
                "query": query,
                "expected_section": expected_section,
                "expected_rank": expected_rank,
                "top1_pass": top1_pass,
                "top3_pass": top3_pass,
                "retrieved_sections": retrieved_sections,
            }
        )

    # ========================================================
    # Calculate Accuracy
    # ========================================================

    total_tests = len(TEST_CASES)

    top1_accuracy = (
        top1_correct / total_tests
    ) * 100

    top3_accuracy = (
        top3_correct / total_tests
    ) * 100

    # ========================================================
    # Print Summary
    # ========================================================

    print()
    print("=" * 70)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 70)

    print(
        f"Total test cases : {total_tests}"
    )

    print(
        f"Top-1 correct    : "
        f"{top1_correct}/{total_tests}"
    )

    print(
        f"Top-1 accuracy   : "
        f"{top1_accuracy:.1f}%"
    )

    print(
        f"Top-{TOP_K} correct  : "
        f"{top3_correct}/{total_tests}"
    )

    print(
        f"Top-{TOP_K} accuracy : "
        f"{top3_accuracy:.1f}%"
    )

    # ========================================================
    # Save Results
    # ========================================================

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    evaluation_output = {
        "evaluation_method": (
            "Exact normalized section heading match"
        ),
        "top_k": TOP_K,
        "total_test_cases": total_tests,
        "top1_correct": top1_correct,
        "top1_accuracy_percent": round(
            top1_accuracy,
            1
        ),
        "top3_correct": top3_correct,
        "top3_accuracy_percent": round(
            top3_accuracy,
            1
        ),
        "test_results": detailed_results,
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation_output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(
        f"Results saved to:\n{OUTPUT_FILE.resolve()}"
    )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()