#!/usr/bin/env python3
"""Get a specific LumeClaw memory by UUID."""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _client import authed_request

def main():
    p = argparse.ArgumentParser(description="Get a LumeClaw memory by UUID")
    p.add_argument("--id", required=True, dest="memory_id", help="Memory UUID")
    args = p.parse_args()

    try:
        m = authed_request("GET", f"/memory/{args.memory_id}")
    except RuntimeError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

    tags = ", ".join(m.get("tags") or [])
    print(f"ID       : {m['id']}")
    print(f"Category : {m['category']}")
    print(f"Tags     : {tags or '(none)'}")
    print(f"Created  : {m.get('created_at','')[:19]}")
    print(f"Updated  : {m.get('updated_at','')[:19]}")
    print(f"\n{m['content']}")

if __name__ == "__main__":
    main()
