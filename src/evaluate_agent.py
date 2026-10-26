"""
Phase 9 - Integrated Agent Evaluation

Evaluates routing and safety behavior against a fixed test set.
This evaluation does not execute transactions.
"""

import json
from pathlib import Path

from phase7_agent import Phase7BankingAgent


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEST_FILE = PROJECT_ROOT / "data" / "evaluation_test_cases.json"


def load_test_cases():
    with open(TEST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_case(agent, test_case):
    result = agent.ask(test_case["question"])

    actual_route = result.get("route", "UNKNOWN")
    expected_route = test_case["expected_route"]

    route_pass = actual_route == expected_route

    return {
        "id": test_case["id"],
        "category": test_case["category"],
        "question": test_case["question"],
        "expected_route": expected_route,
        "actual_route": actual_route,
        "route_pass": route_pass,
        "response": result.get("adapted_answer", ""),
    }


def main():
    print("=" * 80)
    print("PHASE 9 - INTEGRATED AGENT EVALUATION")
    print("=" * 80)

    test_cases = load_test_cases()

    print(f"Loaded evaluation cases: {len(test_cases)}")

    agent = Phase7BankingAgent()

    results = []

    for test_case in test_cases:
        result = evaluate_case(agent, test_case)
        results.append(result)

        status = "PASS" if result["route_pass"] else "FAIL"

        print(
            f"{result['id']} | "
            f"{result['category']} | "
            f"{status} | "
            f"Expected={result['expected_route']} | "
            f"Actual={result['actual_route']}"
        )

    total = len(results)
    passed = sum(1 for result in results if result["route_pass"])
    failed = total - passed

    accuracy = (passed / total) * 100 if total else 0

    print("\n" + "-" * 80)
    print("EVALUATION SUMMARY")
    print("-" * 80)

    print(f"Total tests : {total}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print(f"Route accuracy: {accuracy:.1f}%")

    print("\nFAILURES")

    failures = [
        result
        for result in results
        if not result["route_pass"]
    ]

    if not failures:
        print("No routing failures detected.")
    else:
        for failure in failures:
            print(
                f"{failure['id']} | "
                f"Expected={failure['expected_route']} | "
                f"Actual={failure['actual_route']}"
            )

    print("=" * 80)


if __name__ == "__main__":
    main()