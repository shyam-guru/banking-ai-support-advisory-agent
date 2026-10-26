"""
Phase 6 - Banking Agent with Planning and Short-Term Memory
"""

from memory import ConversationMemory
from planner import BankingPlanner
from tool_router import BankingToolRouter


class Phase6BankingAgent:

    def __init__(self):
        print("[Phase 6] Initializing Banking Agent...")

        self.memory = ConversationMemory(max_turns=5)
        self.planner = BankingPlanner()
        self.router = BankingToolRouter()

        print("[Phase 6] Agent initialized.")

    def resolve_follow_up(self, question):
        """
        Resolve short follow-up questions using the
        previous conversation subject.
        """

        text = question.lower().strip()

        follow_up_patterns = [
            "what should i do first",
            "what should i do",
            "what next",
            "what do i do next",
            "what about that",
            "can you explain that",
            "tell me more"
        ]

        if not any(
            pattern in text
            for pattern in follow_up_patterns
        ):
            return question

        last_turn = self.memory.get_last_turn()

        if not last_turn:
            return question

        subject = last_turn.get("subject")

        if subject == "lost_or_stolen_card":
            return "What should I do if my debit card was stolen?"

        return question

    def process(self, question):
        """
        Process one user question.
        """

        resolved_question = self.resolve_follow_up(question)

        context = self.memory.get_context()

        plan = self.planner.create_plan(
            resolved_question,
            context
        )

        print("\n" + "=" * 70)
        print("USER QUESTION:")
        print(question)

        if resolved_question != question:
            print("\nRESOLVED FOLLOW-UP:")
            print(resolved_question)

        print("\nPLAN:")
        print(f"Intent: {plan['intent']}")
        print(f"Route: {plan['route']}")

        for index, step in enumerate(
            plan["steps"],
            start=1
        ):
            print(f"  {index}. {step}")

        # --------------------------------------------------
        # Use the existing Phase 5 router
        # --------------------------------------------------

        result = self.router.route(resolved_question)

        route = result.get("route")

        print("\nRESULT ROUTE:")
        print(route)

        print("\nANSWER:")
        print(result.get("answer"))

        # --------------------------------------------------
        # Determine safe subject for memory
        # --------------------------------------------------

        subject = None

        if plan["intent"] == "lost_or_stolen_card":
            subject = "lost_or_stolen_card"

        elif plan["intent"] == "customer_profile":
            subject = "customer_profile"

        elif plan["intent"] == "branch_information":
            subject = "branch_information"

        elif plan["intent"] == "money_movement":
            subject = "money_movement"

        elif plan["intent"] == "customer_financial_information":
            subject = "customer_financial_information"

        elif plan["intent"] == "contextual_follow_up":
            previous = self.memory.get_last_turn()

            if previous:
                subject = previous.get("subject")

        # --------------------------------------------------
        # Store only safe conversational metadata
        # --------------------------------------------------

        self.memory.add_turn(
            intent=plan["intent"],
            route=route,
            subject=subject
        )

        return {
            "question": question,
            "resolved_question": resolved_question,
            "plan": plan,
            "route": route,
            "answer": result.get("answer"),
            "memory": self.memory.get_context()
        }


def main():

    agent = Phase6BankingAgent()

    # ---------------------------------------------
    # Phase 6 Test 1
    # ---------------------------------------------

    agent.process(
        "My debit card was stolen."
    )

    # ---------------------------------------------
    # Phase 6 Test 2
    # Context-aware follow-up
    # ---------------------------------------------

    agent.process(
        "What should I do first?"
    )


if __name__ == "__main__":
    main()