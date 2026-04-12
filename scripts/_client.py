"""
Shared HTTP client for Memory LumeClaw skill scripts.
Uses stdlib only — no external dependencies.
"""
import json
import os
import time
import urllib.request
import urllib.error
import urllib.parse
from typing import Any, Optional

API_BASE = os.environ.get("LUMECLAW_API_BASE", "https://skill.lumeclaw.ru/api/v1")
API_KEY  = os.environ.get("LUMECLAW_API_KEY", "")

# ── Low-level request ─────────────────────────────────────────────────────────

def api_request(method: str, path: str, body: Any = None,
                token: Optional[str] = None) -> Any:
    url = API_BASE.rstrip("/") + "/" + path.lstrip("/")
    data = json.dumps(body).encode() if body is not None else None
    headers: dict = {"Accept": "application/json"}
    if data:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"{token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            if not raw:
                return None
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read())
            detail = err.get("detail", str(err))
        except Exception:
            detail = str(e)
        raise RuntimeError(f"HTTP {e.code}: {detail}")


def get_token() -> str:
    if not API_KEY:
        raise RuntimeError(
            "Set LUMECLAW_API_KEY environment variable via your platform dashboard.\n"
            "Register at https://memory.lumeclaw.ru"
        )
    return API_KEY


def authed_request(method: str, path: str, body: Any = None) -> Any:
    token = get_token()
    return api_request(method, path, body, token=token)
