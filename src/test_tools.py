"""
Phase 5 - Tool Integration Test

Tests the read-only tools independently before
connecting them to the Banking AI agent.
"""

from customer_profile_tool import CustomerProfileTool
from branch_service_tool import BranchServiceTool


def main():

    print("=" * 70)
    print("PHASE 5 - READ-ONLY TOOLS TEST")
    print("=" * 70)

    # ---------------------------------------------------------
    # Tool 1: Customer Profile
    # ---------------------------------------------------------

    customer_tool = CustomerProfileTool()

    print("\n[TEST 1] Customer Profile Lookup")
    print("-" * 70)

    customer = customer_tool.lookup("CUST001")

    print(customer)

    # ---------------------------------------------------------
    # Tool 2: Unknown Customer
    # ---------------------------------------------------------

    print("\n[TEST 2] Unknown Customer")
    print("-" * 70)

    unknown_customer = customer_tool.lookup("CUST999")

    print(unknown_customer)

    # ---------------------------------------------------------
    # Tool 3: Branch Information
    # ---------------------------------------------------------

    branch_tool = BranchServiceTool()

    print("\n[TEST 3] Branch Information")
    print("-" * 70)

    branch = branch_tool.get_branch("Chennai Main Branch")

    print(branch)

    # ---------------------------------------------------------
    # Tool 4: Unknown Branch
    # ---------------------------------------------------------

    print("\n[TEST 4] Unknown Branch")
    print("-" * 70)

    unknown_branch = branch_tool.get_branch("Unknown Branch")

    print(unknown_branch)

    print("\n" + "=" * 70)
    print("PHASE 5 TOOL TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()