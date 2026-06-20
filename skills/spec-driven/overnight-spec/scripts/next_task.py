#!/usr/bin/env python3
"""
Deterministic task selector for the one-task overnight Execute sub-mode. Parses a
tasks.md checklist and emits the FIRST unchecked task as JSON — the model
implements it, but the SCRIPT decides which one (zero tokens, no free
association). One task per run is the hard bound that keeps an overnight loop
from draining the backlog or overbaking into scope creep.

tasks.md is expected to contain GitHub-style checklist items, optionally with a
stable id and target files in trailing tags:

    ## tasks
    - [ ] T1: add input validation to parser  (files: src/parse.ts)
    - [x] T2: write failing test for empty input
    - [ ] T3: handle the empty-input case  (files: src/parse.ts, test/parse.test.ts)

Emits {done, total, remaining, next: {id, title, files, raw} | null}. When
next is null, the backlog is empty (the loop should no-op and report).

Usage:
  python next_task.py --tasks .specs/features/<feature>/tasks.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys

CHECK_RE = re.compile(r"^\s*[-*]\s*\[(?P<mark>[ xX])\]\s*(?P<body>.+?)\s*$")
ID_RE = re.compile(r"^(?P<id>[A-Za-z]+\d+|\d+)[:.\)]\s*(?P<rest>.+)$")
FILES_RE = re.compile(r"\(files?:\s*(?P<files>[^)]+)\)", re.I)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Select the first unchecked task from a tasks.md checklist.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--tasks", required=True, help="Path to tasks.md.")
    return p.parse_args()


def parse_task(body: str, index: int) -> dict:
    files: list[str] = []
    fm = FILES_RE.search(body)
    title = body
    if fm:
        files = [f.strip() for f in fm.group("files").split(",") if f.strip()]
        title = FILES_RE.sub("", body).strip()
    idm = ID_RE.match(title)
    task_id = idm.group("id") if idm else f"task-{index}"
    if idm:
        title = idm.group("rest").strip()
    return {"id": task_id, "title": title, "files": files, "raw": body}


def main() -> int:
    args = parse_args()
    try:
        lines = open(args.tasks, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(json.dumps({"error": f"could not read tasks: {e}", "next": None}))
        return 1

    done = 0
    total = 0
    next_task = None
    for i, line in enumerate(lines, 1):
        m = CHECK_RE.match(line)
        if not m:
            continue
        total += 1
        if m.group("mark").lower() == "x":
            done += 1
        elif next_task is None:
            next_task = parse_task(m.group("body"), i)

    result = {
        "done": done,
        "total": total,
        "remaining": total - done,
        "next": next_task,
    }
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
