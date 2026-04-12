#!/usr/bin/env python3
"""Store a memory entry in LumeClaw."""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import authed_request

def main():
    p = argparse.ArgumentParser(description="Store memory in LumeClaw")
    p.add_argument("--content", required=True, help="Text to remember")
    p.add_argument("--category", default="personal",
                   choices=["personal", "project", "server", "preferences"])
    p.add_argument("--tags", default="", help="Comma-separated tags")
    p.add_argument("--agent-id", help="Agent UUID (optional)")
    p.add_argument("--project-id", help="Project UUID (optional)")
    args = p.parse_args()

    payload = {
        "content": args.content,
        "category": args.category,
        "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
    }
    if args.agent_id:
        payload["agent_id"] = args.agent_id
    if args.project_id:
        payload["project_id"] = args.project_id

    try:
        resp = authed_request("POST", "/memory", payload)
        print(f"✅ Stored: [{resp['id']}]")
        print(f"   Category : {resp['category']}")
        print(f"   Tags     : {', '.join(resp.get('tags') or [])}")
        print(f"   Content  : {resp['content'][:200]}")
    except RuntimeError as e:
        if "409" in str(e) or "duplicate" in str(e).lower():
            print("ℹ️  Memory already exists (duplicate content skipped)")
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
