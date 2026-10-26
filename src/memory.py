"""
Phase 6 - Short-Term Conversation Memory

Stores only safe conversational metadata needed to resolve
short-term follow-up questions.

This module intentionally does NOT store:
- passwords
- PINs
- CVVs
- OTPs
- full card numbers
- account balances
- transaction details
- other sensitive authentication information
"""


class ConversationMemory:
    """
    Lightweight short-term memory for the banking agent.

    The memory stores recent interaction metadata rather than
    complete user messages.
    """

    def __init__(self, max_turns=5):
        self.max_turns = max_turns
        self.turns = []

    def add_turn(
        self,
        intent,
        route,
        subject=None,
        customer_id=None
    ):
        """
        Store safe metadata from the latest interaction.
        """

        turn = {
            "intent": intent,
            "route": route,
            "subject": subject,
            "customer_id": customer_id
        }

        self.turns.append(turn)

        # Keep only the most recent turns.
        self.turns = self.turns[-self.max_turns:]

    def get_last_turn(self):
        """
        Return the most recent interaction.
        """

        if not self.turns:
            return None

        return self.turns[-1]

    def get_context(self):
        """
        Return a compact representation of recent context.
        """

        return list(self.turns)

    def clear(self):
        """
        Clear the current conversation memory.
        """

        self.turns.clear()

    def has_context(self):
        """
        Return True if conversation context exists.
        """

        return len(self.turns) > 0