"""
Phase 5 - Banking AI Tool Router

Routes user questions to the appropriate READ-ONLY capability.

Available capabilities:
    1. RAG - Banking policy knowledge
    2. Customer Profile Tool - synthetic customer data
    3. Branch / Service Tool - synthetic branch information

IMPORTANT:
    No transaction, payment, transfer, approval, or account
    modification tool is available.
"""

import re

from customer_profile_tool import CustomerProfileTool
from branch_service_tool import BranchServiceTool
from rag_agent import BankingRAGAgent


class BankingToolRouter:
    """
    Safety-first router for the Banking AI Support Agent.
    """

    def __init__(self):

        self.customer_tool = CustomerProfileTool()
        self.branch_tool = BranchServiceTool()
        self.rag_agent = BankingRAGAgent(top_k=3)

    # ---------------------------------------------------------
    # Safety checks
    # ---------------------------------------------------------

    def is_transaction_request(self, question: str) -> bool:

        text = question.lower()

        transaction_terms = [
            "transfer",
            "send money",
            "move money",
            "pay",
            "payment",
            "withdraw",
            "deposit",
            "approve loan",
            "approve the loan",
            "approve my loan",
            "approve a loan",
            "loan approval",
            "authorize transaction",
            "execute transaction"
        ]

        return any(term in text for term in transaction_terms)

    def is_sensitive_customer_request(self, question: str) -> bool:

        text = question.lower()

        sensitive_terms = [
            "balance",
            "account balance",
            "transaction history",
            "transactions",
            "has money",
            "money in",
            "funds",
            "available funds",
            "how much money",
            "how much is in",
            "amount in the account",
            "pin",
            "cvv",
            "otp",
            "password",
            "full card number"
        ]

        return any(term in text for term in sensitive_terms)

    def is_sensitive_authentication_request(self, question: str) -> bool:
        text = question.lower()

        authentication_terms = [
            "pin",
            "cvv",
            "otp",
            "password",
            "full card number",
            "card number",
            "security code",
        ]

        return any(term in text for term in authentication_terms)

    def is_legal_advice_request(self, question: str) -> bool:
        text = question.lower()

        legal_terms = [
            "legal advice",
            "legal rights",
            "lawyer",
            "attorney",
            "legal dispute",
            "legal action",
            "sue the bank",
            "lawsuit",
        ]

        return any(term in text for term in legal_terms)

    # ---------------------------------------------------------
    # Customer ID detection
    # ---------------------------------------------------------

    def extract_customer_id(self, question: str):

        match = re.search(
            r"\bCUST\d{3}\b",
            question.upper()
        )

        if match:
            return match.group(0)

        return None

    # ---------------------------------------------------------
    # Branch detection
    # ---------------------------------------------------------

    def is_branch_request(self, question: str) -> bool:

        text = question.lower()

        branch_terms = [
            "branch",
            "services available",
            "services offered",
            "what services"
        ]

        return any(term in text for term in branch_terms)

    # ---------------------------------------------------------
    # Customer profile request detection
    # ---------------------------------------------------------

    def is_customer_profile_request(self, question: str) -> bool:

        text = question.lower()

        profile_terms = [
            "account type",
            "type of account",
            "what type of account",
            "account status",
            "which account",
            "customer profile",
            "eligible services",
            "registered branch",
            "which branch",
            "customer branch"
        ]

        return any(term in text for term in profile_terms)

    # ---------------------------------------------------------
    # Main routing method
    # ---------------------------------------------------------

    def route(self, question: str):

        question = question.strip()

        # -----------------------------------------------------
        # 1. Specific loan-approval safety check
        # -----------------------------------------------------

        text = question.lower()

        if (
            "loan approval" in text
            or "approve my loan" in text
            or "approve a loan" in text
            or "approve the loan" in text
            or ("approve" in text and "loan" in text)
        ):

            return {
                "route": "SAFETY_REFUSAL",
                "answer": (
                    "I cannot approve, authorize, or make lending decisions "
                    "on a loan application. Loan approval must be handled "
                    "through the bank's authorized lending process."
                )
            }

        # -----------------------------------------------------
        # 2. Transaction safety check
        # -----------------------------------------------------

        if self.is_transaction_request(question):

            return {
                "route": "SAFETY_REFUSAL",
                "answer": (
                    "I cannot initiate, authorize, approve, or execute "
                    "financial transactions. Please use the bank's "
                    "authorized transaction channel for money movement."
                )
            }

        # -----------------------------------------------------
        # 2. Sensitive authentication information
        # -----------------------------------------------------

        if self.is_sensitive_authentication_request(question):

            return {
                "route": "SAFETY_REFUSAL",
                "answer": (
                    "I cannot provide or request PINs, CVVs, OTPs, passwords, "
                    "or full card numbers. Please use the bank's authorized "
                    "support channel."
                )
            }

        # -----------------------------------------------------
        # 3. Legal advice
        # -----------------------------------------------------

        if self.is_legal_advice_request(question):

            return {
                "route": "SAFETY_REFUSAL",
                "answer": (
                    "I cannot provide legal advice. For advice about your "
                    "legal rights or a banking dispute, consult a qualified "
                    "legal professional or the appropriate official "
                    "dispute-resolution channel."
                )
            }

        # -----------------------------------------------------
        # 4. Customer-specific request
        # -----------------------------------------------------

        customer_id = self.extract_customer_id(question)

        if customer_id:

            # Sensitive financial information is not available
            # through this read-only synthetic profile tool.

            if self.is_sensitive_customer_request(question):

                return {
                    "route": "CUSTOMER_DATA_UNAVAILABLE",
                    "customer_id": customer_id,
                    "answer": (
                        "The available synthetic customer profile does "
                        "not contain this financial information, so I "
                        "cannot provide it. Please use an authorized "
                        "banking channel for account-specific financial "
                        "information."
                    )
                }

            if self.is_customer_profile_request(question):

                result = self.customer_tool.lookup(customer_id)

                if result.get("found") is False:

                    return {
                        "route": "CUSTOMER_LOOKUP",
                        "customer_id": customer_id,
                        "answer": (
                            f"No approved customer profile was found "
                            f"for {customer_id}."
                        )
                    }

                return {
                    "route": "CUSTOMER_LOOKUP",
                    "customer_id": customer_id,
                    "data": result,
                    "answer": self.format_customer_response(result)
                }

        # -----------------------------------------------------
        # 5. Branch / service request
        # -----------------------------------------------------

        if self.is_branch_request(question):

            branches = self.branch_tool.list_branches()

            # Try to identify a specific branch.
            question_lower = question.lower()

            for branch in branches:

                if branch["branch_name"].lower() in question_lower:

                    return {
                        "route": "BRANCH_LOOKUP",
                        "data": branch,
                        "answer": self.format_branch_response(branch)
                    }

            # If no specific branch is identified,
            # return all supported branches.

            return {
                "route": "BRANCH_LOOKUP",
                "data": branches,
                "answer": self.format_all_branches_response(branches)
            }

        # -----------------------------------------------------
        # 6. Otherwise use RAG
        # -----------------------------------------------------

        result = self.rag_agent.answer(question)

        return {
            "route": "RAG",
            "answer": result["answer"],
            "sources": result["sources"]
        }

    # ---------------------------------------------------------
    # Response formatting
    # ---------------------------------------------------------

    def format_customer_response(self, customer):

        services = ", ".join(customer["eligible_services"])

        return (
            f"Customer {customer['customer_id']} has a "
            f"{customer['account_type']} account with status "
            f"{customer['account_status']}. The registered branch is "
            f"{customer['branch']}. Available services include: "
            f"{services}."
        )

    def format_branch_response(self, branch):

        services = ", ".join(branch["services"])

        return (
            f"{branch['branch_name']} in {branch['city']} "
            f"provides: {services}."
        )

    def format_all_branches_response(self, branches):

        responses = []

        for branch in branches:

            services = ", ".join(branch["services"])

            responses.append(
                f"{branch['branch_name']} ({branch['city']}): "
                f"{services}."
            )

        return "\n".join(responses)


if __name__ == "__main__":

    router = BankingToolRouter()

    print("=" * 70)
    print("PHASE 5 - BANKING TOOL ROUTER")
    print("=" * 70)

    test_questions = [

        "What type of account does CUST001 have?",

        "What services are available at Chennai Main Branch?",

        "What is the balance of CUST001?",

        "Transfer ₹50,000 from my account.",

        "What should I do if my debit card was stolen?"
    ]

    for question in test_questions:

        print("\n" + "-" * 70)
        print("QUESTION:")
        print(question)

        result = router.route(question)

        print("\nROUTE:")
        print(result["route"])

        print("\nANSWER:")
        print(result["answer"])