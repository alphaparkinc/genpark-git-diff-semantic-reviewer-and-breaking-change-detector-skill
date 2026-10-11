"""MCP server for Git Diff Semantic Reviewer."""
import sys
import json
from client import GitDiffSemanticReviewer

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "review_git_diff",
                "description": "Reviews unified git diffs for breaking signature changes and leaked credentials",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "diff_text": {"type": "string"}
                    },
                    "required": ["diff_text"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "review_git_diff":
            diff_text = params.get("arguments", {}).get("diff_text", "")
            res = GitDiffSemanticReviewer.review_diff(diff_text)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
