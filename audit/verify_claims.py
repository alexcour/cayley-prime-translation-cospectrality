#!/usr/bin/env python3
"""Check claim evidence without upgrading mathematical, priority or review status."""
import hashlib
import json
import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
registry = root / "audit" / "CLAIMS.json"
errors = []
try:
    data = json.loads(registry.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    claims = data["claims"]
    assert len({c["id"] for c in claims}) == len(claims)
    for claim in claims:
        p = root / claim["proof"]
        if not p.is_file() or not p.resolve().is_relative_to(root.resolve()):
            errors.append(f"{claim['id']}: missing or unsafe proof path")
            continue
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        if actual != claim["proof_sha256"]:
            errors.append(f"{claim['id']}: SHA256 mismatch {actual}")
        if claim["external_review"] != "OPEN":
            errors.append(f"{claim['id']}: review promotion requires separate signed audit")
        if claim["priority_status"] != "N_NON_AUDITEE":
            errors.append(f"{claim['id']}: priority promotion forbidden by this pilot")
        if claim["formal_proof"] != "NOT_ATTESTED":
            errors.append(f"{claim['id']}: formal proof is not attested")
        if not claim.get("obligations"):
            errors.append(f"{claim['id']}: no proof obligations")
    assert {c["id"] for c in claims} == {"10A6", "10C3", "10B1"}
except (OSError, ValueError, KeyError, AssertionError) as exc:
    errors.append(f"Invalid claims registry: {exc}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)
print("Claim evidence OK: 3 raw-byte SHA256 matches; no scientific gate promoted")
