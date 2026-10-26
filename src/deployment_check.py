"""
Phase 8 - Deployment Readiness Checks

Validates the local deployment environment before the
Banking AI Support & Advisory Agent is started.

The checks do not expose secrets or customer information.
"""

import os
from pathlib import Path

from config import OPENAI_ENABLED, OPENAI_API_KEY, OPENAI_MODEL


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PATHS = [
    PROJECT_ROOT / "data" / "knowledge_base" / "banking_policies.md",
    PROJECT_ROOT / "data" / "faiss_index" / "banking.index",
    PROJECT_ROOT / "data" / "faiss_index" / "chunks.json",
]


def check_environment():
    """
    Check deployment configuration and required files.
    """

    results = []

    # --------------------------------------------------
    # 1. OpenAI configuration
    # --------------------------------------------------

    if OPENAI_ENABLED:

        if OPENAI_API_KEY:
            results.append(
                ("OPENAI_CONFIGURATION", "PASS")
            )
        else:
            results.append(
                ("OPENAI_CONFIGURATION", "FAIL")
            )

    else:

        results.append(
            ("OPENAI_CONFIGURATION", "PASS - OpenAI disabled")
        )

    # --------------------------------------------------
    # 2. Model configuration
    # --------------------------------------------------

    if OPENAI_MODEL:

        results.append(
            ("MODEL_CONFIGURATION", "PASS")
        )

    else:

        results.append(
            ("MODEL_CONFIGURATION", "FAIL")
        )

    # --------------------------------------------------
    # 3. Required project files
    # --------------------------------------------------

    for path in REQUIRED_PATHS:

        if path.exists():

            results.append(
                (
                    f"REQUIRED_FILE: {path.name}",
                    "PASS"
                )
            )

        else:

            results.append(
                (
                    f"REQUIRED_FILE: {path.name}",
                    "FAIL"
                )
            )

    return results


def run_deployment_check():

    print("=" * 70)
    print("PHASE 8 - DEPLOYMENT READINESS CHECK")
    print("=" * 70)

    results = check_environment()

    failures = 0

    for name, status in results:

        print(f"{name}: {status}")

        if status == "FAIL":
            failures += 1

    print("\n" + "-" * 70)

    if failures == 0:

        print("DEPLOYMENT READINESS: PASS")
        print(
            "All required configuration and deployment files "
            "are available."
        )

    else:

        print("DEPLOYMENT READINESS: FAIL")
        print(
            f"{failures} deployment check(s) failed."
        )

    print("=" * 70)

    return failures == 0


if __name__ == "__main__":
    run_deployment_check()