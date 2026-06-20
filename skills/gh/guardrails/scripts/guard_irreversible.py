#!/usr/bin/env python3
"""
PreToolUse hook: deterministically DENY tier-2 (irreversible) operations during
any autonomous / unattended run. Generalized, config-driven version of the
maintenance guard — shared by every across-time skill (watch-pr, overnight-spec,
research-digest).

This is defense-in-depth, NOT the primary control. The primary control is to run
the routine without the capability at all (no merge scope, no write connector —
see references/autonomy-boundary.md). A string matcher on shell commands is a
tripwire, not a sandbox.

Behavior:
  - Reads the PreToolUse payload from stdin.
  - Loads an optional boundary config (.claude/autonomy-boundary.json) for EXTRA
    deny patterns; always enforces the built-in tier-2 defaults.
  - On a positive match, prints the current-schema deny decision and exits 0.
  - On no match, stays silent (exit 0 = no opinion).
  - If a present config file is unparseable, fails CLOSED for the dangerous
    defaults (still denies the built-ins) and notes the bad config on stderr.

Wire via .claude/settings.json (matcher "Bash") — see references/settings.example.json.
"""

from __future__ import annotations

import json
import os
import re
import sys

# Built-in tier-2 defaults: always denied in an unattended run.
DEFAULT_PATTERNS: list[tuple[str, str]] = [
    ("merge a pull request", r"\bgh\s+pr\s+merge\b"),
    ("merge via the GraphQL API", r"mergePullRequest"),
    ("approve a pull request", r"\bgh\s+pr\s+review\b.*--approve"),
    ("force-push", r"\bgit\s+push\b.*(--force\b|--force-with-lease|\s-f\b|\+)"),
    ("delete a remote branch", r"\bgit\s+push\b.*(--delete\b|\s:\S)"),
    ("delete a branch", r"\bgit\s+branch\s+-[dD]\b"),
    ("push to a protected branch", r"\bgit\s+push\b.*\b(origin\s+)?(main|master|release)\b"),
    ("deploy without dry-run", r"\blexflow\s+deploy\b(?!.*--dry-run)"),
    ("recursive force delete", r"\brm\s+-[a-z]*r[a-z]*f|\brm\s+-[a-z]*f[a-z]*r"),
    ("recursive force delete (PowerShell)", r"Remove-Item\b.*-Recurse\b.*-Force|Remove-Item\b.*-Force\b.*-Recurse"),
]

CONFIG_NAME = "autonomy-boundary.json"


def load_extra_patterns() -> list[tuple[str, str]]:
    # Look for .claude/autonomy-boundary.json relative to CWD; optional.
    path = os.path.join(".claude", CONFIG_NAME)
    if not os.path.exists(path):
        return []
    try:
        cfg = json.loads(open(path, encoding="utf-8").read())
        out = []
        for entry in cfg.get("deny_patterns", []):
            label = entry.get("label", "a blocked operation")
            pattern = entry.get("pattern")
            if pattern:
                out.append((label, pattern))
        return out
    except (OSError, json.JSONDecodeError, AttributeError):
        print(f"guard_irreversible: could not parse {path}; enforcing built-in defaults only", file=sys.stderr)
        return []


def normalize(command: str) -> str:
    stripped = re.sub(r"^(?:\s*[A-Za-z_][A-Za-z0-9_]*=\S*\s+)+", "", command)
    return re.sub(r"\s+", " ", stripped).strip()


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"Blocked by autonomy guardrail: an unattended run may not {reason}. "
                        "Tier-2 (irreversible) actions are reserved for a human session. "
                        "Do the reversible work and stop; do not attempt to bypass this."
                    ),
                }
            }
        )
    )


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    if not command:
        return 0

    norm = normalize(command)
    patterns = DEFAULT_PATTERNS + load_extra_patterns()
    for reason, pattern in patterns:
        try:
            if re.search(pattern, norm, re.I):
                deny(reason)
                return 0
        except re.error:
            continue
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
