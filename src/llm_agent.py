"""
LLM agent interface.

The rest of the application calls this module rather than
calling OpenAI directly.

The actual provider is selected by llm_provider.py.
"""

from llm_provider import get_llm


class BankingLLMAgent:
    """
    Banking LLM agent.

    The provider can be either:
        - MockLLM
        - OpenAI ChatOpenAI
    """

    def __init__(self):
        self.llm = get_llm()

    def generate(self, prompt: str) -> str:
        """
        Generate a response using the configured LLM.

        Args:
            prompt: Prompt supplied to the LLM.

        Returns:
            Generated response as a string.
        """

        response = self.llm.invoke(prompt)

        # LangChain ChatOpenAI normally returns an
        # AIMessage object containing .content.
        if hasattr(response, "content"):
            return response.content

        # MockLLM returns a normal string.
        return str(response)