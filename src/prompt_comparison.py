"""
Phase 3 - Prompt Comparison

Runs the SAME test set through three different prompts.

Outputs are saved so that they can later be analyzed and
included in the capstone evaluation evidence.
"""

import json
from pathlib import Path

from langchain_openai import ChatOpenAI

from config import OPENAI_MODEL
from prompts import PROMPT_V1, PROMPT_V2, PROMPT_V3


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

TEST_FILE = Path("data/prompt_test_cases.json")

OUTPUT_FILE = Path(
    "evidence/prompt_comparison_results.json"
)


# ---------------------------------------------------------
# Create model
# ---------------------------------------------------------

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0
)


# ---------------------------------------------------------
# Load test cases
# ---------------------------------------------------------

with TEST_FILE.open("r", encoding="utf-8") as file:
    test_cases = json.load(file)


# ---------------------------------------------------------
# Prompt variants
# ---------------------------------------------------------

prompts = {
    "Prompt V1": PROMPT_V1,
    "Prompt V2": PROMPT_V2,
    "Prompt V3": PROMPT_V3
}


# ---------------------------------------------------------
# Run comparison
# ---------------------------------------------------------

results = []

for test in test_cases:

    test_id = test["id"]
    question = test["question"]

    print("\n" + "=" * 70)
    print(f"{test_id}: {question}")
    print("=" * 70)

    test_result = {
        "test_id": test_id,
        "question": question,
        "outputs": {}
    }

    for prompt_name, prompt_template in prompts.items():

        prompt = prompt_template.format(
            question=question
        )

        response = llm.invoke(prompt)

        answer = response.content

        test_result["outputs"][prompt_name] = answer

        print(f"\n--- {prompt_name} ---")
        print(answer)

    results.append(test_result)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with OUTPUT_FILE.open(
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        results,
        file,
        indent=2,
        ensure_ascii=False
    )


print("\n")
print("=" * 70)
print("Prompt comparison completed.")
print(f"Results saved to: {OUTPUT_FILE}")
print("=" * 70)