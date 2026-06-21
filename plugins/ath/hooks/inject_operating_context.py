#!/usr/bin/env python3
"""SessionStart hook: re-establish the toolkit's operating frame at session start
and after a context compaction — exactly when the model has lost the thread.
Emits operating-context.md as `additionalContext`.

Deliberately light and principle-level (not a procedure): it loads on EVERY
session in every repo where the plugin is enabled, so it nudges the way of
working, it does not force a mode. Edit operating-context.md to change the frame.
"""

from __future__ import annotations

import json
import os
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "operating-context.md")
    try:
        ctx = open(path, encoding="utf-8").read().strip()
    except OSError:
        return 0  # no context file -> stay silent, never block the session
    if not ctx:
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": ctx,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
