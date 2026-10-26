"""
Mock LLM provider for development and testing.

IMPORTANT:
These responses are deterministic development responses.
They are NOT actual OpenAI model outputs.

The mock model extracts the CUSTOMER QUESTION from the
RAG prompt before applying its keyword rules. This prevents
retrieved knowledge-base text and safety instructions from
incorrectly triggering a response.
"""


class MockLLM:
    """
    Simple deterministic mock language model.

    The purpose is to test application architecture,
    routing, safety handling, RAG integration, tools,
    and memory without calling an external API.
    """

    def _extract_customer_question(self, prompt: str) -> str:
        """
        Extract the customer question from a RAG prompt.

        Expected prompt structure:

            CUSTOMER QUESTION
            =================

            <actual question>

            ANSWER
            ======

        If the markers are not present, the complete prompt
        is used as a fallback.
        """

        start_marker = "CUSTOMER QUESTION"
        end_marker = "ANSWER"

        if start_marker in prompt:

            question_part = prompt.split(
                start_marker,
                1
            )[1]

            # Remove the separator after the heading.
            if "====" in question_part:

                question_part = question_part.split(
                    "====",
                    1
                )[1]

            # Remove everything after ANSWER.
            if end_marker in question_part:

                question_part = question_part.split(
                    end_marker,
                    1
                )[0]

            return question_part.strip()

        # Fallback for non-RAG prompts
        return prompt.strip()

    def invoke(self, prompt: str) -> str:
        """
        Generate a deterministic development response.

        The keyword matching is performed against the
        customer question rather than the entire RAG prompt.
        """

        # ----------------------------------------------------
        # Extract actual customer question
        # ----------------------------------------------------

        question = self._extract_customer_question(
            prompt
        )

        text = question.lower()

        # ----------------------------------------------------
        # Money movement
        # ----------------------------------------------------

        if (
            "transfer" in text
            or "send money" in text
            or "move money" in text
        ):
            return (
                "I cannot initiate, authorize, approve, or execute "
                "money transfers. Please use the bank's authorized "
                "transaction channel for money movement."
            )

        # ----------------------------------------------------
        # Lost or stolen card
        # ----------------------------------------------------

        if (
            ("lost" in text and "card" in text)
            or ("stolen" in text and "card" in text)
        ):
            return (
                "If your debit card is lost or stolen, contact the "
                "bank through its authorized support channel and "
                "request that the card be blocked or replaced. "
                "Do not share your PIN, CVV, OTP, or full card number."
            )

        # ----------------------------------------------------
        # Unrecognized transaction / fraud
        # ----------------------------------------------------

        if (
            "unrecognized transaction" in text
            or "unauthorized transaction" in text
            or "unknown transaction" in text
            or "unrecognized" in text
            or "unauthorized" in text
            or "fraud" in text
            or "don't recognize" in text
            or "do not recognize" in text
            or "didn't make" in text
            or "did not make" in text
        ):
            return (
                "If you notice an unrecognized or unauthorized "
                "transaction, contact the bank through its official "
                "fraud or customer-support channel promptly and "
                "report the transaction for review. Do not share "
                "your PIN, CVV, OTP, password, or full card number."
            )

        # ----------------------------------------------------
        # Loan approval
        # ----------------------------------------------------

        if (
            "approve" in text
            and "loan" in text
        ):
            return (
                "I cannot approve or authorize a loan application. "
                "Loan decisions must be handled through the bank's "
                "authorized lending process."
            )

        # ----------------------------------------------------
        # Legal advice
        # ----------------------------------------------------

        if (
            "legal advice" in text
            or "lawyer" in text
            or "legal rights" in text
            or "legal action" in text
            or "sue the bank" in text
            or "bank dispute" in text
        ):
            return (
                "I cannot provide legal advice. For advice about "
                "your legal rights or a banking dispute, consult "
                "a qualified legal professional or the appropriate "
                "official dispute-resolution channel."
            )


        # ----------------------------------------------------
        # Sensitive authentication information
        # ----------------------------------------------------

        if (
            "never share" in text
            or "should i never share" in text
            or (
                "share" in text
                and (
                    "pin" in text
                    or "cvv" in text
                    or "otp" in text
                    or "password" in text
                    or "card number" in text
                )
            )
        ):
            return (
                "Never share your password, PIN, CVV, OTP, full card number, "
                "or full account credentials with the chatbot. Use the bank's "
                "authorized authentication or support channel when sensitive "
                "information is required."
            )

        # ----------------------------------------------------
        # Customer financial information
        # ----------------------------------------------------

        if (
            (
                "balance" in text
                or "account balance" in text
                or "transaction history" in text
            )
            and (
                "my" in text
                or "customer" in text
                or "account" in text
            )
        ):
            return (
                "I cannot provide or invent customer financial "
                "information. Customer-specific information must "
                "come from an authorized read-only banking system "
                "or approved customer record."
            )

        # ----------------------------------------------------
        # Replacement fee
        # ----------------------------------------------------

        if (
            "replacement fee" in text
            or "replacement charge" in text
        ):
            return (
                "I do not have a verified fee for this request. "
                "I will not invent a banking fee. The applicable "
                "fee should be verified against the approved "
                "banking policy or fee schedule."
            )

        # ----------------------------------------------------
        # Savings account documentation
        # ----------------------------------------------------

        if (
            "savings account" in text
            and (
                "document" in text
                or "documents" in text
                or "requirement" in text
            )
        ):
            return (
                "The required documents should be verified against "
                "the bank's approved account-opening policy. "
                "I should not invent documentation requirements."
            )

        # ----------------------------------------------------
        # Generic development response
        # ----------------------------------------------------

        return (
            "[MOCK LLM RESPONSE] I can provide a banking support "
            "response when verified knowledge, approved policy, "
            "or an authorized read-only tool provides the required "
            "information."
        )
