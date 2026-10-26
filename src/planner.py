"""
Phase 6 - Banking Request Planner

Creates a simple deterministic execution plan before
the agent performs an action.

The planner does not execute transactions.
"""


class BankingPlanner:

    def create_plan(self, question, context=None):
        """
        Create an execution plan based on the question
        and available short-term context.
        """

        text = question.lower()

        # --------------------------------------------------
        # 1. Money movement
        # --------------------------------------------------

        if any(
            phrase in text
            for phrase in [
                "transfer",
                "send money",
                "move money",
                "pay",
                "payment"
            ]
        ):
            return {
                "intent": "money_movement",
                "route": "SAFETY_REFUSAL",
                "steps": [
                    "Detect money-movement request",
                    "Apply non-transactional safety policy",
                    "Refuse transaction execution",
                    "Direct user to authorized banking channel"
                ]
            }

        # --------------------------------------------------
        # 2. Customer-specific request
        # --------------------------------------------------

        if "cust" in text:
            if any(
                phrase in text
                for phrase in [
                    "balance",
                    "available money",
                    "transaction history",
                    "loan balance",
                    "credit limit"
                ]
            ):
                return {
                    "intent": "customer_financial_information",
                    "route": "CUSTOMER_DATA_UNAVAILABLE",
                    "steps": [
                        "Identify customer-specific financial request",
                        "Check whether approved read-only data is available",
                        "Do not invent unavailable financial information",
                        "Direct user to an authorized banking channel"
                    ]
                }

            return {
                "intent": "customer_profile",
                "route": "CUSTOMER_LOOKUP",
                "steps": [
                    "Extract customer identifier",
                    "Call approved read-only customer profile tool",
                    "Use only returned customer fields",
                    "Generate safe response"
                ]
            }

        # --------------------------------------------------
        # 3. Branch information
        # --------------------------------------------------

        if "branch" in text and any(
            word in text
            for word in [
                "service",
                "services",
                "available",
                "support"
            ]
        ):
            return {
                "intent": "branch_information",
                "route": "BRANCH_LOOKUP",
                "steps": [
                    "Identify branch request",
                    "Call approved read-only branch tool",
                    "Return supported branch services",
                    "Generate concise response"
                ]
            }

        # --------------------------------------------------
        # 4. Lost / stolen card
        # --------------------------------------------------

        if (
            ("lost" in text or "stolen" in text)
            and "card" in text
        ):
            return {
                "intent": "lost_or_stolen_card",
                "route": "RAG",
                "steps": [
                    "Identify lost or stolen card request",
                    "Retrieve approved banking policy",
                    "Generate grounded response",
                    "Include sensitive-information warning"
                ]
            }

        # --------------------------------------------------
        # 5. Follow-up question using memory
        # --------------------------------------------------

        if context:
            last_turn = context[-1]

            if last_turn.get("subject"):
                return {
                    "intent": "contextual_follow_up",
                    "route": last_turn.get("route", "RAG"),
                    "steps": [
                        "Use previous conversation context",
                        "Resolve the follow-up question",
                        "Continue the previous task",
                        "Generate a context-aware response"
                    ]
                }

        # --------------------------------------------------
        # 6. General banking support
        # --------------------------------------------------

        return {
            "intent": "general_banking_support",
            "route": "RAG",
            "steps": [
                "Search approved banking knowledge",
                "Generate grounded response",
                "State uncertainty if information is unavailable"
            ]
        }