#!/usr/bin/env python3
"""Record RPC connectivity separately from error-specific verification."""
import datetime
import json
import os
from pathlib import Path
import urllib.request
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.validate_schema import parse_frontmatter


def rpc_call(rpc_url, method, params=None):
    request = urllib.request.Request(rpc_url, data=json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": method, "params": params or {},
    }).encode(), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            return json.load(response)
    except Exception as error:
        return {"error": {"message": str(error)}}


def verify_entry(entry, rpc_url, latest_ledger, response=None):
    """Connectivity or malformed-input responses never verify a catalog error."""
    if response is None:
        response = rpc_call(rpc_url, "getNetwork")
    return {
        "entry_id": entry["id"], "category": entry["category"],
        "error_code": entry["error_code"], "verified": False,
        "status": "REVIEW_REQUIRED", "network": "testnet",
        "rpc_url": rpc_url, "latest_ledger": latest_ledger,
        "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "details": {"test": "RPC connectivity only", "response": response},
        "review_note": "Requires a valid error-specific reproduction and observed matching execution diagnostics. Network health and malformed XDR rejection are insufficient.",
    }


def main():
    root = Path(__file__).resolve().parents[1]
    url = os.environ.get("SOROBAN_RPC_URL", "https://soroban-testnet.stellar.org")
    response = rpc_call(url, "getNetwork")
    ledger_response = rpc_call(url, "getLatestLedger")
    ledger = ledger_response.get("result", {}).get("sequence", 0)
    results = []
    for path in sorted((root / "entries").rglob("*.md")):
        entry, _ = parse_frontmatter(path.read_text())
        results.append(verify_entry(entry, url, ledger, response))
    # Preserve historical per-entry observations; do not overwrite them with connectivity.
    output = root / "verification" / "connectivity-review.json"
    output.write_text(json.dumps({"verified_count": 0, "entries": results}, indent=2) + "\n")
    print(f"Recorded connectivity for {len(results)} entries; no error-specific verification asserted.")


if __name__ == "__main__":
    main()
