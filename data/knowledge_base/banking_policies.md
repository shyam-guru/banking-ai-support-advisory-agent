# Banking Support Knowledge Base

## Purpose

This document contains fictional and controlled banking support
information for the Banking AI Support & Advisory Agent capstone.

The information is intended only for demonstration and testing.

The agent must not invent information that is not present in
this knowledge base or supplied by an authorized read-only tool.

---

# 1. Lost or Stolen Debit Card

If a customer has lost a debit card or believes that the card
has been stolen, the customer should contact the bank through
an official customer-support channel as soon as possible.

The customer should request that the card be blocked and ask
about the available replacement process.

Customers should never share their PIN, CVV, OTP, password,
or complete card number with a support agent or chatbot.

If the customer suspects that the card has been used without
authorization, the issue should also be treated as a potential
fraud or unauthorized-transaction case.

---

# 2. Debit Card Replacement

A replacement card may be requested when a debit card is lost,
stolen, damaged, or otherwise unusable.

The applicable replacement fee depends on the bank's current
approved fee schedule.

The Banking AI Support Agent must not invent or guess a
replacement fee.

If the exact replacement fee is not available in the approved
knowledge base, the customer should be directed to the bank's
official fee schedule or customer-support channel.

---

# 3. Unrecognized or Unauthorized Transactions

If a customer notices a transaction that they do not recognize,
they should contact the bank through its official fraud or
customer-support channel promptly.

The customer should review the transaction details through an
authorized banking channel.

The customer must not provide their PIN, CVV, OTP, password,
or complete card number to the chatbot.

Cases involving suspected fraud, account compromise, or
unauthorized transactions should be treated as higher-risk
support cases and may require escalation.

The Banking AI Support Agent must not claim that a transaction
is fraudulent unless sufficient verified information is available.

---

# 4. Savings Account Opening

Customers who want to open a savings account should refer to
the bank's approved account-opening process.

The exact documentation requirements may vary depending on the
account type and applicable banking requirements.

The Banking AI Support Agent must provide only documentation
requirements that are available in the approved knowledge base.

If the required documentation information is unavailable,
the agent should say that it cannot verify the requirement and
direct the customer to the bank's official account-opening
channel.

---

# 5. Loan Information

The Banking AI Support Agent may provide general information
about loan products when that information is available in the
approved knowledge base.

The agent must not approve, reject, authorize, or modify a
loan application.

Loan decisions must be handled through the bank's authorized
lending process.

The agent must not claim that a customer is eligible for a
loan unless eligibility information has been explicitly
provided by an authorized system.

---

# 6. Money Transfers

The banking support assistant is non-transactional.

It must not:
- Initiate a money transfer
- Execute a money transfer
- Authorize a money transfer
- Approve a money transfer
- Move money between accounts
- Provide confirmation that a transfer has been completed

Money-transfer requests include:
- "Transfer ₹50,000 from my account."
- "Send money to another account."
- "Move ₹10,000 to my savings account."
- "Make a bank transfer for me."
- "Can you transfer money on my behalf?"

For a money-transfer request, the assistant must refuse the transactional action and direct the customer to the bank's authorized transaction channel.

The assistant may provide general information about how money transfers work when that information is available in the approved knowledge base.

The assistant must never claim that a transfer was initiated, authorized, approved, processed, or completed.

---

# 7. Customer-Specific Information

The banking support assistant must not invent, guess, or disclose customer-specific financial information.

Customer-specific information includes:
- Current account balance
- Available account balance
- Account number
- Customer account details
- Transaction history
- Deposits and withdrawals
- Loan balance
- Credit limit
- Personal financial information

The assistant may provide customer-specific information only when an approved read-only customer information tool supplies the information for the authenticated request.

If the required customer information is not available through an approved tool, the assistant must clearly state that it cannot access or verify the information.

Examples of customer-specific requests include:
- "What is my current account balance?"
- "What is my available balance?"
- "How much money do I have in my account?"
- "Show me my recent transactions."
- "What is my loan balance?"

The assistant must never guess or fabricate a customer's balance, account details, or transaction history.

---

# 8. Legal Advice

The banking support assistant must not provide legal advice or act as a lawyer.

Legal-advice requests include:
- Requests for legal advice about a bank dispute
- Questions about legal rights against a bank
- Questions about filing legal proceedings against a bank
- Requests to interpret a legal agreement or contract
- Requests for advice about litigation
- Requests for advice about legal claims
- Requests asking what a customer should legally do in a dispute
- Requests for a lawyer's or attorney's opinion

Examples include:
- "Can you give me legal advice about a dispute with my bank?"
- "What legal action should I take against my bank?"
- "Can I sue the bank?"
- "What are my legal rights in this dispute?"
- "Should I file a legal case against the bank?"

For such requests, the assistant must clearly state that it cannot provide legal advice.

The assistant may provide general factual information from the approved banking knowledge base, but must not present that information as legal advice.

When appropriate, the customer should be directed to a qualified legal professional or the bank's authorized grievance/support channel.

---

# 9. Authentication and Sensitive Information

The chatbot must never ask a customer to provide:

- password
- PIN
- CVV
- OTP
- full card number
- full account credentials

Sensitive authentication information must not be stored in
application logs.

If a customer voluntarily provides sensitive information,
the application should avoid reproducing it in the response
and should follow the appropriate safety handling procedure.

---

# 10. Escalation

The following situations should normally be escalated or
directed to an authorized banking support channel:

- suspected fraud
- unauthorized transactions
- account compromise
- requests for money movement
- requests for transaction authorization
- requests for loan approval
- requests involving unavailable customer data
- requests requiring legal advice
- ambiguous high-risk requests
- situations where the approved knowledge base does not
  contain sufficient information

The agent should be transparent about uncertainty rather than
inventing an answer.

---

# 11. Knowledge Grounding Rule

The Banking AI Support Agent should follow this principle:

If verified information exists in the approved knowledge base
or an authorized read-only tool, use it.

If the required information is unavailable, do not guess.

Instead:

1. state that the information cannot be verified;
2. ask for clarification when appropriate; or
3. direct the customer to the appropriate official channel.

---

# 12. Scope of the Capstone

This capstone demonstrates a non-transactional banking support
and advisory assistant.

The system is intended to:

- answer general banking support questions
- retrieve approved knowledge
- use authorized read-only tools
- maintain short-term conversation context
- provide safe responses
- identify situations requiring escalation

The system is not intended to perform financial transactions
or make binding banking decisions.