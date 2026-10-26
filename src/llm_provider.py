"""
LLM provider abstraction.

The application uses this module instead of directly depending
on OpenAI.

Current development mode:
    OPENAI_ENABLED=false
    -> MockLLM

Future production/evaluation mode:
    OPENAI_ENABLED=true
    -> OpenAI ChatOpenAI
"""

from config import (
    OPENAI_ENABLED,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

from mock_llm import MockLLM


def get_llm():
    """
    Return the configured LLM provider.

    Returns:
        MockLLM when OpenAI is disabled.
        ChatOpenAI when OpenAI is enabled.
    """

    # -----------------------------------------------------
    # Development mode
    # -----------------------------------------------------

    if not OPENAI_ENABLED:
        print("[LLM] OpenAI disabled. Using MockLLM.")
        return MockLLM()

    # -----------------------------------------------------
    # OpenAI mode
    # -----------------------------------------------------

    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_ENABLED=true but OPENAI_API_KEY is missing."
        )

    from langchain_openai import ChatOpenAI

    print(f"[LLM] Using OpenAI model: {OPENAI_MODEL}")

    return ChatOpenAI(
        model=OPENAI_MODEL,
        temperature=0,
        api_key=OPENAI_API_KEY,
    )