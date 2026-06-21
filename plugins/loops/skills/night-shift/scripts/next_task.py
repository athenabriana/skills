#!/usr/bin/env python3
"""
Deterministic task selector for the one-task overnight Execute sub-mode. Parses
the shape file's task checklist and emits the FIRST unchecked task as JSON — the
model implements it, but the SCRIPT decides which one (zero tokens, no free
association). One task per run is the hard bound that keeps an overnight loop
from draining the backlog or overbaking into scope creep.

The shape file is a single `.shape/<slug>.md` (brief + tasks in one file). Tasks
live under a `## tasks` heading as GitHub-style checklist items, optionally with
a stable id and target files in trailing tags:

    # build the thing
    ...brief prose, decisions, what we're NOT doing...

    ## tasks
    - [ ] T1: add input validation to parser  (files: src/parse.ts)
    - [x] T2: write failing test for empty input
    - [ ] T3: handle the empty-input case  (files: src/parse.ts, test/parse.test.ts)

Only checkboxes under the tasks heading count — checkbox-looking lines elsewhere
in the brief (e.g. an open-questions list) are ignored. If the file has no tasks
heading, the whole file is scanned (back-compat with a bare task list).

Emits {done, total, remaining, next: {id, title, files, raw} | null}. When
next is null, the backlog is empty (the loop should no-op and report).

Usage:
  python next_task.py --tasks .shape/<slug>.md
  python next_task.py --self-test
"""

from __future__ import annotations

import argparse
import json
import sys

import re

CHECK_RE = re.compile(r"^\s*[-*]\s*\[(?P<mark>[ xX])\]\s*(?P<body>.+?)\s*$")
ID_RE = re.compile(r"^(?P<id>[A-Za-z]+\d+|\d+)[:.\)]\s*(?P<rest>.+)$")
FILES_RE = re.compile(r"\(files?:\s*(?P<files>[^)]+)\)", re.I)
HEADING_RE = re.compile(r"^\s*#{1,6}\s+(?P<text>.+?)\s*$")
TASKS_HEADING_RE = re.compile(r"^\s*#{1,6}\s+tasks\b", re.I)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Select the first unchecked task from a shape file's tasks section.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--tasks", help="Path to the shape file (.shape/<slug>.md).")
    p.add_argument("--self-test", action="store_true", help="Run built-in tests and exit.")
    return p.parse_args()


def tasks_section(lines: list[str]) -> list[str]:
    """Return only the lines inside the `## tasks` section. If there is no tasks
    heading, return all lines (a bare checklist file)."""
    start = None
    for i, line in enumerate(lines):
        if TASKS_HEADING_RE.match(line):
            start = i + 1
            break
    if start is None:
        return lines
    out: list[str] = []
    for line in lines[start:]:
        if HEADING_RE.match(line):  # next heading ends the section
            break
        out.append(line)
    return out


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


def select(lines: list[str]) -> dict:
    done = 0
    total = 0
    next_task = None
    for i, line in enumerate(tasks_section(lines), 1):
        m = CHECK_RE.match(line)
        if not m:
            continue
        total += 1
        if m.group("mark").lower() == "x":
            done += 1
        elif next_task is None:
            next_task = parse_task(m.group("body"), i)
    return {"done": done, "total": total, "remaining": total - done, "next": next_task}


def self_test() -> int:
    merged = [
        "# build the thing",
        "open questions:",
        "- [ ] should NOT be picked (outside tasks section)",
        "",
        "## tasks",
        "- [x] T1: scaffold  (files: a.ts)",
        "- [ ] T2: validate input  (files: src/parse.ts)",
        "- [ ] T3: handle empty case",
        "",
        "## notes",
        "- [ ] also ignored (after tasks section)",
    ]
    r = select(merged)
    assert r["total"] == 3, r
    assert r["done"] == 1, r
    assert r["next"]["id"] == "T2", r
    assert r["next"]["files"] == ["src/parse.ts"], r

    bare = ["- [x] done one", "- [ ] do two"]  # no tasks heading -> whole file
    r2 = select(bare)
    assert r2["total"] == 2 and r2["next"]["title"] == "do two", r2

    empty = ["## tasks", "- [x] all done"]
    assert select(empty)["next"] is None

    print("next_task self-test: PASS (3/3)")
    return 0


def main() -> int:
    args = parse_args()
    if args.self_test:
        return self_test()
    if not args.tasks:
        print(json.dumps({"error": "--tasks is required", "next": None}))
        return 2
    try:
        lines = open(args.tasks, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(json.dumps({"error": f"could not read shape file: {e}", "next": None}))
        return 1
    print(json.dumps(select(lines), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
