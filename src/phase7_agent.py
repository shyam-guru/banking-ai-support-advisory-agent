"""
Phase 7 - Banking Agent with Feedback-Based Adaptation
"""

from adaptation import FeedbackAdapter
from tool_router import BankingToolRouter


class Phase7BankingAgent:

    def __init__(self):

        print("[Phase 7] Initializing Adaptive Banking Agent...")

        self.router = BankingToolRouter()
        self.adapter = FeedbackAdapter()

        print("[Phase 7] Adaptive Banking Agent initialized.")

    def ask(self, question):
        """
        Answer a question using the existing Phase 5 router
        and apply the current response-style preference.
        """

        print("\n" + "=" * 70)
        print("USER QUESTION: [REDACTED]")

        result = self.router.route(question)

        original_answer = result.get("answer", "")

        adapted_answer = self.adapter.adapt_response(
            original_answer
        )

        print("\nCURRENT RESPONSE STYLE:")
        print(self.adapter.get_preference())

        print("\nANSWER:")
        print(adapted_answer)

        return {
            "question": question,
            "route": result.get("route"),
            "original_answer": original_answer,
            "adapted_answer": adapted_answer,
            "response_style": self.adapter.get_preference()
        }

    def give_feedback(self, feedback):
        """
        Process user feedback and update the session
        response preference.
        """

        result = self.adapter.process_feedback(
            feedback
        )

        print("\n" + "-" * 70)
        print("USER FEEDBACK:")
        print(feedback)

        print("\nADAPTATION:")
        print(result["adaptation"])

        print("\nMESSAGE:")
        print(result["message"])

        print("\nCURRENT RESPONSE STYLE:")
        print(self.adapter.get_preference())

        return result