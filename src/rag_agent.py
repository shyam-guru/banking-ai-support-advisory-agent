"""
Banking AI - Retrieval-Augmented Generation Agent

Pipeline:

User Query
    ↓
FAISS Retriever
    ↓
Top-K Knowledge Chunks
    ↓
Grounded Context
    ↓
Safety + Grounding Prompt
    ↓
LLM Provider
    ↓
Banking Response

The LLM provider is selected through llm_provider.py.

When OPENAI_ENABLED=false, the project uses MockLLM.
When OpenAI is enabled later, the same RAG pipeline can
use ChatOpenAI without changing the retrieval logic.
"""

from retrieval import BankingRetriever
from llm_provider import get_llm


# ============================================================
# Configuration
# ============================================================

TOP_K = 3


# ============================================================
# RAG Agent
# ============================================================

class BankingRAGAgent:

    def __init__(self, top_k=TOP_K):

        print(
            "[RAG] Initializing Banking RAG Agent..."
        )

        self.retriever = BankingRetriever(
            top_k=top_k
        )

        self.llm = get_llm()

        self.top_k = top_k

        print(
            "[RAG] Banking RAG Agent initialized."
        )

    # ========================================================
    # Build Context
    # ========================================================

    def build_context(self, results):

        context_parts = []

        for rank, result in enumerate(
            results,
            start=1
        ):

            section = result.get(
                "section",
                "Unknown"
            )

            content = result.get(
                "content",
                ""
            )

            context_parts.append(
                f"""
SOURCE {rank}
Section: {section}
Similarity Score: {result['score']:.4f}

{content}
""".strip()
            )

        return "\n\n".join(
            context_parts
        )

    # ========================================================
    # Build Prompt
    # ========================================================

    def build_prompt(
        self,
        question,
        context
    ):

        prompt = f"""
You are a Banking AI Support & Advisory Agent.

Your role is limited to non-transactional banking support.

Use ONLY the supplied knowledge-base context to answer
the customer's question.

IMPORTANT SAFETY RULES:

1. Do not invent banking policies, fees, account information,
   customer information, transaction information, or product
   information.

2. Do not execute, initiate, authorize, approve, or confirm
   any financial transaction.

3. Do not provide legal advice.

4. Do not request or expose passwords, PINs, CVVs, OTPs,
   full card numbers, or full account credentials.

5. Do not claim access to customer-specific information unless
   an approved customer-information tool explicitly provides it.

6. If the knowledge base does not contain enough information,
   clearly state that the information is unavailable and
   recommend an appropriate authorized support channel.

7. For fraud, unauthorized transactions, account compromise,
   or other high-risk situations, recommend contacting the
   bank through an authorized support channel.

8. Keep the answer concise, clear, and professional.

KNOWLEDGE-BASE CONTEXT
======================

{context}

CUSTOMER QUESTION
=================

{question}

ANSWER
======
"""

        return prompt.strip()

    # ========================================================
    # Generate Response
    # ========================================================

    def answer(self, question):

        print()
        print(
            "[RAG] Retrieving knowledge..."
        )

        results = self.retriever.search(
            question
        )

        if not results:

            return {
                "question": question,
                "answer": (
                    "I could not find relevant information "
                    "in the approved banking knowledge base. "
                    "Please contact the bank through an "
                    "authorized support channel."
                ),
                "sources": [],
            }

        # ----------------------------------------------------
        # Build grounded context
        # ----------------------------------------------------

        context = self.build_context(
            results
        )

        # ----------------------------------------------------
        # Build LLM prompt
        # ----------------------------------------------------

        prompt = self.build_prompt(
            question,
            context
        )

        # ----------------------------------------------------
        # Generate answer
        # ----------------------------------------------------

        print(
            "[RAG] Generating grounded response..."
        )

        response = self.llm.invoke(
            prompt
        )

        # ----------------------------------------------------
        # Handle different LLM response formats
        # ----------------------------------------------------

        if hasattr(
            response,
            "content"
        ):

            answer_text = response.content

        else:

            answer_text = str(
                response
            )

        # ----------------------------------------------------
        # Store source information
        # ----------------------------------------------------

        sources = []

        for rank, result in enumerate(
            results,
            start=1
        ):

            sources.append(
                {
                    "rank": rank,
                    "section": result.get(
                        "section",
                        ""
                    ),
                    "score": round(
                        result["score"],
                        4
                    ),
                    "source": result.get(
                        "source",
                        ""
                    ),
                }
            )

        return {
            "question": question,
            "answer": answer_text,
            "sources": sources,
        }


# ============================================================
# Interactive Test
# ============================================================

def main():

    print("=" * 70)
    print("BANKING AI - RAG AGENT TEST")
    print("=" * 70)

    agent = BankingRAGAgent(
        top_k=TOP_K
    )

    test_questions = [

        "What should I do if my debit card was stolen?",

        "Can you transfer ₹50,000 from my account?",

        "Can you give me legal advice about a dispute with my bank?",

        "What information should I never share with the chatbot?",
    ]

    for question in test_questions:

        print()
        print("=" * 70)
        print(
            f"QUESTION: {question}"
        )
        print("=" * 70)

        result = agent.answer(
            question
        )

        print()
        print("ANSWER:")
        print(result["answer"])

        print()
        print("SOURCES:")

        for source in result["sources"]:

            print(
                f"  {source['rank']}. "
                f"{source['section']} "
                f"(score={source['score']})"
            )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    main()