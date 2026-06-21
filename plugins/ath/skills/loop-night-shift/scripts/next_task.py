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
    ...brief prose, decisions, out-of-scope bullets (NOT checkboxes)...

    ## tasks
    - [ ] T1: add input validation to parser  (files: src/parse.ts)
    - [x] T2: write failing test for empty input
    - [ ] T3: handle the empty-input case  (files: src/parse.ts, test/parse.test.ts)
    - [ ] T4: flaky integration  (blocked: needs staging creds)

Selection rules:
  - Only checkboxes UNDER the tasks heading count. If the file has headings but
    no tasks heading, that's a brief with no task list → no-op (we never scan a
    structured doc's stray checkboxes). A file with no headings at all is treated
    as a bare checklist (back-compat).
  - A task tagged `(blocked: ...)` is skipped and counted, so a poison task can't
    be re-attempted every night — mark it blocked and the loop moves on.
  - Lines that look like a checkbox but don't parse (e.g. `-[ ]`, `- [] x`) are
    reported in `warnings` so a typo doesn't silently drop a task.

Emits {done, total, blocked, remaining, warnings, next: {id, title, files, raw}
| null}. When next is null, there is nothing actionable (the loop no-ops and
reports). An `error` field (with next=null) means the file could not be used.

Usage:
  python next_task.py --tasks .shape/<slug>.md
  python next_task.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re

CHECK_RE = re.compile(r"^\s*[-*]\s*\[(?P<mark>[ xX])\]\s*(?P<body>.+?)\s*$")
# Looks like a checkbox to a human but won't parse above — flag, don't drop.
NEARMISS_RE = re.compile(r"^\s*[-*]?\s*\[[^\]]?\]")
ID_RE = re.compile(r"^(?P<id>[A-Za-z]+\d+|\d+)[:.\)]\s*(?P<rest>.+)$")
FILES_RE = re.compile(r"\(files?:\s*(?P<files>[^)]+)\)", re.I)
BLOCKED_RE = re.compile(r"\(blocked\b", re.I)
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


def tasks_section(lines: list[str]) -> list[str] | None:
    """Lines inside the `## tasks` section. None means 'no usable task list':
    headings exist but none is a tasks heading. A file with no headings at all
    falls back to the whole file (a bare checklist)."""
    start = None
    has_heading = False
    for i, line in enumerate(lines):
        if HEADING_RE.match(line):
            has_heading = True
        if TASKS_HEADING_RE.match(line):
            start = i + 1
            break
    if start is None:
        return lines if not has_heading else None
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
    section = tasks_section(lines)
    if section is None:
        return {
            "done": 0, "total": 0, "blocked": 0, "remaining": 0,
            "warnings": [], "next": None,
            "error": "no `## tasks` section found in shape file",
        }
    done = blocked = total = 0
    warnings: list[str] = []
    next_task = None
    for i, line in enumerate(section, 1):
        m = CHECK_RE.match(line)
        if not m:
            if NEARMISS_RE.match(line):
                warnings.append(f"line {i}: looks like a checkbox but did not parse: {line.strip()!r}")
            continue
        total += 1
        body = m.group("body")
        if m.group("mark").lower() == "x":
            done += 1
        elif BLOCKED_RE.search(body):
            blocked += 1
        elif next_task is None:
            next_task = parse_task(body, i)
    return {
        "done": done,
        "total": total,
        "blocked": blocked,
        "remaining": total - done - blocked,
        "warnings": warnings,
        "next": next_task,
    }


def self_test() -> int:
    merged = [
        "# build the thing",
        "out of scope:",
        "- ship the mobile app (revisit)",  # plain bullet, must NOT count
        "",
        "## tasks",
        "- [x] T1: scaffold  (files: a.ts)",
        "- [ ] T2: validate input  (files: src/parse.ts)",
        "- [ ] T3: handle empty case",
        "- [ ] T4: flaky  (blocked: needs creds)",
        "- [] T5: empty brackets",  # near-miss -> warning, not a task
        "",
        "## notes",
        "- [ ] ignored (after tasks section)",
    ]
    r = select(merged)
    assert r["total"] == 4, r          # T1..T4; T5 not parsed, notes excluded
    assert r["done"] == 1, r
    assert r["blocked"] == 1, r
    assert r["next"]["id"] == "T2", r  # T4 skipped as blocked
    assert r["remaining"] == 2, r
    assert any("T5" in w or "typo" in w for w in r["warnings"]), r

    structured_no_tasks = ["# brief", "## decisions", "- [ ] not a task"]
    assert select(structured_no_tasks)["next"] is None
    assert "no `## tasks`" in select(structured_no_tasks)["error"]

    bare = ["- [x] done one", "- [ ] do two"]  # no headings -> whole file
    assert select(bare)["next"]["title"] == "do two"

    assert select(["## tasks", "- [x] all done"])["next"] is None

    print("next_task self-test: PASS (4/4)")
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
