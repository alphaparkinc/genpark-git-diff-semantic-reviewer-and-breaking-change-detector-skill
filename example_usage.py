"""Example usage for Git Diff Semantic Reviewer."""
from client import GitDiffSemanticReviewer

if __name__ == "__main__":
    diff = "--- a/api.py\n+++ b/api.py\n-def fetch_user(user_id):\n+def fetch_user(user_id, tenant_id):\n"
    res = GitDiffSemanticReviewer.review_diff(diff)
    print("Merge Status:", res["merge_status"])
    print("Breaking Changes:", res["breaking_changes"])
