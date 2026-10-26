"""
Synthetic Customer Profile Tool

This tool provides READ-ONLY access to fictional customer
profile information for the Banking AI Capstone.

It must never modify customer data and must never invent
financial information such as balances or transactions.
"""

import json
from pathlib import Path


CUSTOMER_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "customer_data"
    / "customers.json"
)


class CustomerProfileTool:
    """
    Read-only lookup tool for synthetic customer profiles.
    """

    def __init__(self):
        with open(CUSTOMER_FILE, "r", encoding="utf-8") as file:
            self.customers = json.load(file)

    def lookup(self, customer_id: str):
        """
        Retrieve a synthetic customer profile by customer ID.
        """

        customer_id = customer_id.strip().upper()

        for customer in self.customers:
            if customer["customer_id"] == customer_id:

                # Return only approved non-sensitive fields.
                return {
                    "customer_id": customer["customer_id"],
                    "customer_name": customer["customer_name"],
                    "account_type": customer["account_type"],
                    "account_status": customer["account_status"],
                    "branch": customer["branch"],
                    "eligible_services": customer["eligible_services"],
                }

        return {
            "customer_id": customer_id,
            "found": False,
            "message": "Customer profile was not found."
        }


if __name__ == "__main__":

    tool = CustomerProfileTool()

    print("=" * 60)
    print("CUSTOMER PROFILE TOOL TEST")
    print("=" * 60)

    print("\nCUST001:")
    print(tool.lookup("CUST001"))

    print("\nUnknown customer:")
    print(tool.lookup("CUST999"))