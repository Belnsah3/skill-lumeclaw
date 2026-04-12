#!/usr/bin/env python3
"""Search LumeClaw memory using semantic similarity."""
import argparse
import sys
import os
import urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
from _client import authed_request

def main():
    p = argparse.ArgumentParser(description="Search LumeClaw memory")
    p.add_argument("--query", required=True, help="Search query")
    p.add_argument("--limit", type=int, default=5, help="Max results (default 5)")
    p.add_argument("--category", choices=["personal", "project", "server", "preferences"])
    p.add_argument("--agent-id")
    args = p.parse_args()

    params = f"query={urllib.parse.quote(args.query)}&limit={args.limit}"
    if args.category:
        params += f"&category={args.category}"
    if args.agent_id:
        params += f"&agent_id={args.agent_id}"

    try:
        results = authed_request("GET", f"/memory/search?{params}")
    except RuntimeError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not results:
        print("No matching memories found.")
        return

    print(f"🔍 Found {len(results)} result(s) for: {args.query!r}\n")
    for i, m in enumerate(results, 1):
        score_pct = round(float(m.get("score", 0)) * 100, 1)
        print(f"{i}. [{score_pct}% | {m['category']}] {m['content'][:250]}")
        if m.get("tags"):
            print(f"   Tags: {', '.join(m['tags'])}")
        print(f"   ID: {m['id']} | {m.get('created_at','')[:10]}")
        print()

if __name__ == "__main__":
    main()
