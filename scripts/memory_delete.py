#!/usr/bin/env python3
"""Delete a LumeClaw memory entry by UUID."""
import argparse
import sys
import os
import urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from _client import get_token, API_BASE

def main():
    p = argparse.ArgumentParser(description="Delete a LumeClaw memory")
    p.add_argument("--id", required=True, dest="memory_id", help="Memory UUID")
    p.add_argument("--yes", action="store_true", help="Skip confirmation")
    args = p.parse_args()

    if not args.yes:
        confirm = input(f"Delete memory {args.memory_id}? [y/N] ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

    token = get_token()
    url = API_BASE.rstrip("/") + f"/memory/{args.memory_id}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        method="DELETE",
    )
    try:
        with urllib.request.urlopen(req, timeout=30):
            pass
        print(f"✅ Deleted memory {args.memory_id}")
    except urllib.request.HTTPError as e:
        if e.code == 404:
            print(f"Memory {args.memory_id} not found")
        else:
            print(f"❌ HTTP {e.code}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
