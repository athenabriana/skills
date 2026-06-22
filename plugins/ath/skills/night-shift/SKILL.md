---
name: night-shift
description: Run ONE pre-shaped task overnight as a desired-state cron-once loop, ending at a draft PR you review in the morning — never a continuous while-true, never an auto-merge. Reloads a committed .ath/tasks/ task list, picks the single next task deterministically, implements only it, runs the local gate, commits to a claude/ branch, opens a DRAFT PR, and stops. Use when the user says "run the overnight queue", "do one small task overnight", or "set up the nightly draft-PR loop". Do NOT use without a committed .ath/tasks/ task list (run /ath:shape-idea first), for open-ended "improve the codebase" work, or to merge (that stays human).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.2.0
---

# Night Shift (cron-once, draft-PR only)

The canonical safe across-time pattern for an EXISTING codebase: a desired-state
loop run **once on a schedule**, doing **one small reviewable task**, leaving a
**draft PR** for the morning. "One small thing every morning beats none — or
fifty." Explicitly NOT a continuous `while-true` Ralph loop (which research says
not to run on brownfield repos) and explicitly NOT an auto-merge.

This skill is the engine; `references/routine-recipe.md` is how to schedule it as
a Cloud Routine. It builds on `/ath:shape-idea` (the brief + sliced tasks) and the
plugin's guard hook (the safety layer, in `hooks/` — auto-active, no install).

## Prerequisites

- A `/ath:shape-idea` brief committed as `.ath/tasks/<slug>/shape.md` with a `## tasks` checklist. A Cloud Routine clones fresh with no local files, so `.ath/tasks/` MUST be committed for the run to see it. If there is no ready task list, the run NO-OPs and reports.
- The plugin's guard hook active (it ships in `hooks/`, auto-active) and its self-test passing (the first step below).

## Workflow (one iteration = one task)

1. **Guard self-test (gate).** Run the plugin's guard self-test (`hooks/selftest_guard.py`). If it fails, ABORT — do not run unguarded.
2. **Pick ONE task.** `python scripts/next_task.py --tasks .ath/tasks/<slug>.md` → the first unchecked task `{id, title, files}` from the file's `## tasks` section (zero tokens; the script decides which, never the model). If `next` is null, no-op and report "backlog empty".
3. **Implement ONLY that task**, honoring the re-shape safety valve: if implementing the one task reveals **>5 emergent steps**, STOP, formalize them into the `## tasks` section (or hand back to `/ath:shape-idea`), and report — do not expand scope.
4. **Stay in the smart zone.** Do file discovery in a read-only sub-agent that returns a ~1–2k-token brief; the single writer edits with a clean context. If the scope brief comes back empty (a grep miss), ABORT rather than concluding the code is unimplemented and duplicating it.
5. **Run the local gate** (lint/format/typecheck/tests) until clean, capped like ath:ship Phase 5: at most **3 log-gated retries**, and only on a known-flake signature — a real failure short-circuits to "halt + report".
6. **Commit to a `claude/` (or `auto/`) branch, open a DRAFT PR** (chain to `/ath:ship` for title/body), check the task's box in the `## tasks` section of `.ath/tasks/<slug>/shape.md`, and **STOP**. You review and merge in the morning.

## Guardrails

- **One task per run** — `next_task.py` returns exactly one, so a misfire can't drain the backlog or overbake into scope creep.
- **Intra-task scope ceiling.** One-task-per-run does NOT bound the SIZE of that task. Set a hard `max-files` / `max-diff-lines` ceiling in the routine prompt; if the task would exceed it, stop and open the partial draft PR rather than gold-plating (a routine runs with no mid-run human to stop it).
- **Draft-PR only, never merge.** The land step stays human. Withhold merge capability from the routine (`ath:hooks/autonomy-boundary.md`); the PreToolUse hook is the backstop.
- **Own circuit breaker.** After N consecutive failed gate runs, write the blocker into the task list / PR and exit. This is your own counter — NOT the Auto Mode breaker (that counts denied actions and does not fire inside a no-prompt routine).
- **Quarantine a poison task.** If a task fails the gate repeatedly across runs, append a `(blocked: <reason>)` tag to its line. `next_task.py` skips blocked tasks (and counts them), so the same broken task can't be re-attempted every single night — the loop moves to the next one and you triage the blocked one by hand.
- **Halt loud.** The worst overnight outcome is "no progress + a clear blocker note", never a runaway or a fabricated fix.
- **Cost.** Single-agent only inside the loop (no fan-out — ~15× tokens compounds per iteration) until a week of usage is measured at claude.ai. Cron-once per night.

## Bundled Resources

### scripts/next_task.py
Parses the `## tasks` section of `.ath/tasks/<slug>/shape.md` and emits the first unchecked, non-blocked task as JSON (`{done, total, blocked, remaining, warnings, next}`) — the deterministic one-task selector. No-ops if the file has headings but no `## tasks` section; skips `(blocked: …)` tasks; warns on malformed checkboxes.

### references/routine-recipe.md
The Cloud Routine setup: commit `.ath/tasks/`, withhold merge scope, the guard hook + probe, the draft-PR-only prompt with the scope ceiling, and the cost cap.
