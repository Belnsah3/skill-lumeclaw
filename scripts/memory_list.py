#!/usr/bin/env python3
"""List LumeClaw memory entries."""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import authed_request

def main():
    p = argparse.ArgumentParser(description="List LumeClaw memories")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--category", choices=["personal", "project", "server", "preferences"])
    p.add_argument("--agent-id")
    args = p.parse_args()

    params = f"limit={args.limit}&offset={args.offset}"
    if args.category:
        params += f"&category={args.category}"
    if args.agent_id:
        params += f"&agent_id={args.agent_id}"

    try:
        memories = authed_request("GET", f"/memory?{params}")
    except RuntimeError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not memories:
        print("No memories found.")
        return

    print(f"📋 {len(memories)} memories:\n")
    for m in memories:
        ts = m.get("created_at", "")[:10]
        tags = f" [{', '.join(m['tags'])}]" if m.get("tags") else ""
        print(f"[{m['id']}] ({ts}) <{m['category']}>{tags}")
        print(f"   {m['content'][:180]}")
        print()

if __name__ == "__main__":
    main()
