import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from customer_profile_tool import CustomerProfileTool
from branch_service_tool import BranchServiceTool


class TestCustomerProfileTool(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tool = CustomerProfileTool()

    def test_known_customer_returns_approved_fields(self):
        result = self.tool.lookup("CUST001")

        self.assertEqual(result["customer_id"], "CUST001")
        self.assertEqual(result["account_type"], "Savings")
        self.assertEqual(result["account_status"], "Active")
        self.assertEqual(result["branch"], "Chennai Main Branch")

        # The read-only tool must not expose balances or transactions.
        self.assertNotIn("balance", result)
        self.assertNotIn("transactions", result)

    def test_customer_id_is_normalized(self):
        result = self.tool.lookup("  cust001  ")
        self.assertEqual(result["customer_id"], "CUST001")

    def test_unknown_customer_is_not_found(self):
        result = self.tool.lookup("CUST999")

        self.assertFalse(result["found"])
        self.assertEqual(
            result["message"],
            "Customer profile was not found.",
        )


class TestBranchServiceTool(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tool = BranchServiceTool()

    def test_known_branch_returns_services(self):
        result = self.tool.get_branch("Chennai Main Branch")

        self.assertEqual(result["branch_name"], "Chennai Main Branch")
        self.assertEqual(result["city"], "Chennai")
        self.assertIn("Debit Card Services", result["services"])

    def test_branch_name_matching_is_case_insensitive(self):
        result = self.tool.get_branch("  chennai main branch  ")
        self.assertEqual(result["branch_name"], "Chennai Main Branch")

    def test_unknown_branch_is_not_found(self):
        result = self.tool.get_branch("Unknown Branch")

        self.assertFalse(result["found"])
        self.assertEqual(
            result["message"],
            "Branch information was not found.",
        )

    def test_list_branches_returns_supported_branches(self):
        result = self.tool.list_branches()
        names = {branch["branch_name"] for branch in result}

        self.assertEqual(
            names,
            {
                "Chennai Main Branch",
                "Chennai Anna Nagar Branch",
                "Chennai Adyar Branch",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
