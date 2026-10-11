"""Git Diff Semantic Reviewer & Breaking Change Detector.
100% Python Standard Library.
"""

import re

class GitDiffSemanticReviewer:
    """Analyzes unified git diffs to flag breaking function signatures, removed exports, and leaked secrets."""

    SECRET_REGEX = r"(ghp_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})"

    @classmethod
    def review_diff(cls, diff_text: str) -> dict:
        removed_defs = []
        added_defs = []
        leaked_secrets = []

        for line in diff_text.splitlines():
            if line.startswith("-") and not line.startswith("---"):
                m = re.search(r"def\s+([a-zA-Z0-9_]+)\((.*?)\):", line)
                if m and not m.group(1).startswith("_"):
                    removed_defs.append({"func": m.group(1), "params": m.group(2)})
            elif line.startswith("+") and not line.startswith("+++"):
                m = re.search(r"def\s+([a-zA-Z0-9_]+)\((.*?)\):", line)
                if m:
                    added_defs.append({"func": m.group(1), "params": m.group(2)})
                if re.search(cls.SECRET_REGEX, line):
                    leaked_secrets.append("Potential API token or credential detected in added line")

        added_map = {d["func"]: d["params"] for d in added_defs}
        breaking_changes = []
        for rem in removed_defs:
            fn = rem["func"]
            if fn not in added_map:
                breaking_changes.append(f"Public function '{fn}' was removed without replacement.")
            elif added_map[fn] != rem["params"]:
                breaking_changes.append(f"Public function '{fn}' changed signature from ({rem['params']}) to ({added_map[fn]}).")

        status = "BLOCK_MERGE" if (leaked_secrets or breaking_changes) else "READY_TO_MERGE"
        return {
            "merge_status": status,
            "breaking_changes": breaking_changes,
            "secret_alerts": leaked_secrets,
            "review_score": max(0, 100 - 40 * len(leaked_secrets) - 25 * len(breaking_changes))
        }
