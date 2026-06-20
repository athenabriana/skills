#!/usr/bin/env python3
"""
Active self-test for the irreversible-op guard. Fires known-bad probe payloads
through guard_irreversible.py and asserts each is DENIED; fires a benign one and
asserts it is allowed. Exits non-zero on any mismatch.

Run this as the FIRST step of any unattended run (and, for a cloud routine, as a
probe `Run now`): if the guard is not actually wired/honored, the run must abort
rather than proceed unguarded. An unwired hook is the ultimate bypass.

Usage:
  python selftest_guard.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

GUARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "guard_irreversible.py")

DENY_PROBES = [
    "gh pr merge 1 --squash",
    "FOO=bar gh pr merge 2",
    "git push --force origin feature",
    "gh pr review 3 --approve",
    "git push origin main",
]
ALLOW_PROBES = [
    "git status",
    "gh pr checks 4 --json name,state",
    "python scripts/scan_repo.py --repo owner/name",
]


def probe(command: str) -> bool:
    """Return True if the guard DENIED the command."""
    payload = json.dumps({"tool_name": "Bash", "tool_input": {"command": command}})
    p = subprocess.run([sys.executable, GUARD], input=payload, capture_output=True, text=True)
    out = (p.stdout or "").strip()
    if not out:
        return False
    try:
        return json.loads(out).get("hookSpecificOutput", {}).get("permissionDecision") == "deny"
    except json.JSONDecodeError:
        return False


def main() -> int:
    failures = 0
    for cmd in DENY_PROBES:
        denied = probe(cmd)
        print(f"[{'PASS' if denied else 'FAIL'}] should DENY: {cmd}", file=sys.stderr)
        if not denied:
            failures += 1
    for cmd in ALLOW_PROBES:
        denied = probe(cmd)
        print(f"[{'PASS' if not denied else 'FAIL'}] should ALLOW: {cmd}", file=sys.stderr)
        if denied:
            failures += 1
    total = len(DENY_PROBES) + len(ALLOW_PROBES)
    print(f"--- guard self-test: {total - failures}/{total} passed", file=sys.stderr)
    if failures:
        print("GUARD SELF-TEST FAILED — abort the unattended run.", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
