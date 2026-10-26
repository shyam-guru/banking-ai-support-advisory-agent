"""
Phase 6 - Planning and Memory Test
"""

from phase6_agent import Phase6BankingAgent


def main():

    print("=" * 70)
    print("PHASE 6 - PLANNING + MEMORY TEST")
    print("=" * 70)

    agent = Phase6BankingAgent()

    # --------------------------------------------------
    # TEST 1 - Initial request
    # --------------------------------------------------

    print("\n[TEST 1] Initial Context")
    print("-" * 70)

    result1 = agent.process(
        "My debit card was stolen."
    )

    # --------------------------------------------------
    # TEST 2 - Contextual follow-up
    # --------------------------------------------------

    print("\n[TEST 2] Context-Aware Follow-Up")
    print("-" * 70)

    result2 = agent.process(
        "What should I do first?"
    )

    # --------------------------------------------------
    # TEST 3 - Customer profile planning
    # --------------------------------------------------

    print("\n[TEST 3] Customer Lookup Planning")
    print("-" * 70)

    result3 = agent.process(
        "What type of account does CUST001 have?"
    )

    # --------------------------------------------------
    # TEST 4 - Safety planning
    # --------------------------------------------------

    print("\n[TEST 4] Transaction Safety Planning")
    print("-" * 70)

    result4 = agent.process(
        "Transfer ₹50,000 from my account."
    )

    # --------------------------------------------------
    # TEST 5 - Safe Short-Term Memory Inspection
    # --------------------------------------------------

    print("\n[TEST 5] Safe Short-Term Memory")
    print("-" * 70)

    print("Stored conversation metadata:")

    for index, turn in enumerate(
        agent.memory.get_context(),
        start=1
    ):
        print(f"Turn {index}: {turn}")

    print("\nMemory safety check:")

    sensitive_terms = [
        "password",
        "pin",
        "cvv",
        "otp",
        "card_number",
        "balance",
        "transaction_history"
    ]

    memory_text = str(agent.memory.get_context()).lower()

    unsafe_items = [
        term
        for term in sensitive_terms
        if term in memory_text
    ]

    if unsafe_items:
        print("FAIL - Sensitive information detected in memory:")
        print(unsafe_items)
    else:
        print(
            "PASS - Memory contains only safe conversational metadata."
        )

    print("\n" + "=" * 70)
    print("PHASE 6 TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
