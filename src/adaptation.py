"""
Phase 7 - Feedback-Based Response Adaptation

This module learns safe response-style preferences from
user feedback.

The adaptation layer can change presentation style but
must never change:
- banking policy
- safety rules
- customer data
- transaction permissions
- tool permissions
"""


class FeedbackAdapter:

    def __init__(self):
        # Session-level response preference.
        self.response_style = "standard"

    def process_feedback(self, feedback):
        """
        Interpret user feedback and update the response style.
        """

        text = feedback.lower().strip()

        # --------------------------------------------------
        # Step-by-step preference
        # --------------------------------------------------

        if any(
            phrase in text
            for phrase in [
                "step by step",
                "step-by-step",
                "give me the steps",
                "give me clear steps",
                "list the steps",
                "actionable steps"
            ]
        ):
            self.response_style = "step_by_step"

            return {
                "feedback": feedback,
                "adaptation": "step_by_step",
                "message": "Response style adapted to step-by-step guidance."
            }

        # --------------------------------------------------
        # Concise preference
        # --------------------------------------------------

        if any(
            phrase in text
            for phrase in [
                "be concise",
                "more concise",
                "keep it short",
                "shorter answer",
                "brief answer"
            ]
        ):
            self.response_style = "concise"

            return {
                "feedback": feedback,
                "adaptation": "concise",
                "message": "Response style adapted to concise responses."
            }

        # --------------------------------------------------
        # Detailed preference
        # --------------------------------------------------

        if any(
            phrase in text
            for phrase in [
                "more detail",
                "give more details",
                "explain in detail",
                "detailed explanation"
            ]
        ):
            self.response_style = "detailed"

            return {
                "feedback": feedback,
                "adaptation": "detailed",
                "message": "Response style adapted to detailed responses."
            }

        # --------------------------------------------------
        # No recognized preference
        # --------------------------------------------------

        return {
            "feedback": feedback,
            "adaptation": "no_change",
            "message": "No supported response-style preference detected."
        }

    def get_preference(self):
        """
        Return the current response-style preference.
        """

        return self.response_style

    def adapt_response(self, response):
        """
        Adapt presentation style without changing the
        underlying information or safety content.
        """

        if self.response_style == "standard":
            return response

        if self.response_style == "concise":
            return self._make_concise(response)

        if self.response_style == "step_by_step":
            return self._make_step_by_step(response)

        if self.response_style == "detailed":
            return self._make_detailed(response)

        return response

    def _make_concise(self, response):
        """
        Keep the first two meaningful sentences.
        """

        sentences = [
            sentence.strip()
            for sentence in response.replace("\n", " ").split(".")
            if sentence.strip()
        ]

        if len(sentences) <= 2:
            return response

        return ". ".join(sentences[:2]) + "."

    def _make_step_by_step(self, response):
        """
        Convert the response sentences into numbered steps.

        This is a presentation change only. No new banking
        facts are added.
        """

        sentences = [
            sentence.strip()
            for sentence in response.replace("\n", " ").split(".")
            if sentence.strip()
        ]

        if not sentences:
            return response

        return "\n".join(
            f"{index}. {sentence}."
            for index, sentence in enumerate(
                sentences,
                start=1
            )
        )

    def _make_detailed(self, response):
        """
        Preserve the original response and add a neutral
        presentation label. The adapter does not invent
        additional banking facts.
        """

        return (
            "Detailed guidance based on the available approved information:\n\n"
            + response
        )