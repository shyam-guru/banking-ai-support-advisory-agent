"""
Phase 2 - Basic Rule-Based Banking Support Agent

Purpose:
    Establish a simple baseline before introducing an LLM.

The agent:
    1. Accepts user input.
    2. Identifies a small number of banking intents.
    3. Returns predefined responses.
    4. Refuses transaction execution requests.
    5. Logs interactions without storing the original user text.

Important:
    This is intentionally NOT an intelligent agent.
    Its limitations will be evaluated and documented.
"""

import json
import re
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

LOG_FILE = Path("logs/interactions.jsonl")


# ---------------------------------------------------------
# PII Protection
# ---------------------------------------------------------

def contains_sensitive_information(text: str) -> bool:
    """
    Performs a simple check for common sensitive information.

    This is NOT a complete PII detector.
    It is only a baseline safety mechanism.
    """

    patterns = [
        r"\b\d{12,19}\b",          # Possible card/account number
        r"\b\d{4,6}\b",            # Possible PIN/OTP
        r"\b\d{3}\b",              # Possible CVV
    ]

    return any(re.search(pattern, text) for pattern in patterns)


# ---------------------------------------------------------
# Intent Detection
# ---------------------------------------------------------

def detect_intent(user_input: str) -> str:
    """
    Detects the user's intent using simple keyword matching.

    This is deliberately basic because this is our baseline.
    """

    text = user_input.lower()

    if any(word in text for word in [
        "transfer money",
        "send money",
        "transfer ₹",
        "transfer rs",
        "move money"
    ]):
        return "money_transfer"

    if (
        "lost" in text and "card" in text
    ) or (
        "stolen" in text and "card" in text
    ):
        return "lost_card"

    if any(word in text for word in [
        "fraud",
        "suspicious transaction",
        "unknown transaction",
        "unauthorized transaction",
        "don't recognize"
    ]):
        return "fraud"

    if any(word in text for word in [
        "open account",
        "opening account",
        "savings account",
        "documents required"
    ]):
        return "account_opening"

    if any(word in text for word in [
        "loan",
        "loan eligibility",
        "loan documents"
    ]):
        return "loan"

    return "unknown"


# ---------------------------------------------------------
# Response Generation
# ---------------------------------------------------------

def generate_response(intent: str) -> str:
    """
    Generates a predefined response based on the detected intent.
    """

    responses = {

        "lost_card":
            "If your debit card is lost or stolen, contact the bank "
            "through its approved customer-support or card-blocking "
            "channel. If you suspect unauthorized activity, the case "
            "should be escalated to the bank's fraud/security team.",

        "fraud":
            "If you notice a transaction that you do not recognize, "
            "contact the bank through its approved fraud or customer "
            "support channel as soon as possible. Do not share your "
            "PIN, password, CVV, or OTP.",

        "account_opening":
            "Account-opening requirements depend on the bank and "
            "account type. Please refer to the approved banking "
            "documentation or contact the bank for the current "
            "requirements.",

        "loan":
            "Loan eligibility, documentation, interest rates, and "
            "approval depend on the specific banking product. "
            "Please refer to the approved product information or "
            "contact the bank for current details.",

        "money_transfer":
            "I cannot initiate, authorize, or execute money transfers. "
            "Please use the bank's authorized transaction channel "
            "for money movement.",

        "unknown":
            "I do not have enough information to answer that banking "
            "question reliably. Please provide more details or "
            "contact an authorized banking representative."
    }

    return responses[intent]


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

def log_interaction(intent: str, response: str, sensitive: bool):
    """
    Logs operational information without storing the user's
    original message.

    This helps demonstrate PII-safe logging.
    """

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "intent": intent,
        "sensitive_input_detected": sensitive,
        "response_length": len(response)
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


# ---------------------------------------------------------
# Main Agent
# ---------------------------------------------------------

def run_agent(user_input: str) -> str:
    """
    Main baseline-agent workflow.
    """

    sensitive = contains_sensitive_information(user_input)

    intent = detect_intent(user_input)

    response = generate_response(intent)

    log_interaction(
        intent=intent,
        response=response,
        sensitive=sensitive
    )

    return response


# ---------------------------------------------------------
# Command-Line Interface
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("Banking AI Support Agent - Phase 2 Baseline")
    print("=" * 60)

    print("Type 'exit' to stop.")

    while True:

        user_input = input("\nUser: ")

        if user_input.lower() == "exit":
            print("Agent: Goodbye.")
            break

        response = run_agent(user_input)

        print(f"\nAgent: {response}")


if __name__ == "__main__":
    main()