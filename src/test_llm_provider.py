"""
Test the LLM provider switching mechanism.

This test should NOT make an OpenAI API call when
OPENAI_ENABLED=false.
"""

from llm_agent import BankingLLMAgent


def main():

    print("=" * 60)
    print("BANKING AI - LLM PROVIDER TEST")
    print("=" * 60)

    agent = BankingLLMAgent()

    test_prompt = """
    User:
    What should I do if my debit card was stolen?

    Provide a safe banking support response.
    """

    response = agent.generate(test_prompt)

    print("\nResponse:")
    print(response)

    print("\nProvider test completed.")


if __name__ == "__main__":
    main()