"""
Branch / Service Information Tool

Provides READ-ONLY information about supported banking
branches and services.

This is synthetic data for the capstone project.
"""

BRANCHES = {
    "chennai_main": {
        "branch_name": "Chennai Main Branch",
        "city": "Chennai",
        "services": [
            "Account Support",
            "Debit Card Services",
            "Online Banking Support",
            "Loan Information"
        ]
    },

    "chennai_anna_nagar": {
        "branch_name": "Chennai Anna Nagar Branch",
        "city": "Chennai",
        "services": [
            "Current Account Services",
            "Savings Account Services",
            "Debit Card Services",
            "Online Banking Support"
        ]
    },

    "chennai_adyar": {
        "branch_name": "Chennai Adyar Branch",
        "city": "Chennai",
        "services": [
            "Account Support",
            "Savings Account Services",
            "Debit Card Services"
        ]
    }
}


class BranchServiceTool:
    """
    Read-only branch and service lookup.
    """

    def list_branches(self):
        """
        Return all supported branches.
        """

        return [
            {
                "branch_name": branch["branch_name"],
                "city": branch["city"],
                "services": branch["services"]
            }
            for branch in BRANCHES.values()
        ]

    def get_branch(self, branch_name: str):
        """
        Retrieve information for a specific branch.
        """

        branch_name = branch_name.strip().lower()

        for branch in BRANCHES.values():

            if branch["branch_name"].lower() == branch_name:

                return {
                    "branch_name": branch["branch_name"],
                    "city": branch["city"],
                    "services": branch["services"]
                }

        return {
            "found": False,
            "message": "Branch information was not found."
        }


if __name__ == "__main__":

    tool = BranchServiceTool()

    print("=" * 60)
    print("BRANCH / SERVICE TOOL TEST")
    print("=" * 60)

    print("\nAll branches:")
    print(tool.list_branches())

    print("\nChennai Main Branch:")
    print(tool.get_branch("Chennai Main Branch"))

    print("\nUnknown branch:")
    print(tool.get_branch("Unknown Branch"))