---
name: implement-idea
description: Implement a validated `.shape/<slug>.md` brief in the working tree — build the slices, run the local gate, commit, and stop ready to ship. Supervised and at-your-desk (the daytime sibling of the overnight loop-night-shift). Use when the user says "implement the brief", "build the shaped tasks", "build it", "implement this", or right after /ath:shape-idea. Do NOT use to shape an idea first (use /ath:shape-idea), to open or green a PR (use /ath:ship), or for an unattended overnight run (use /ath:night-shift).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.0.0
---

# Implement

Build the validated, shaped work in the working tree — supervised, all at once — taking `.shape/<slug>.md` from a brief to code that's ready to ship. The at-desk executor; for unattended one-task-per-night work ending at a draft PR, use `/ath:night-shift`.

## Prerequisites

A validated `.shape/<slug>.md` (brief + a `## tasks` checklist). If there's no shaped brief for this work, stop and suggest `/ath:shape-idea` first — implementing without alignment is exactly what shaping prevents.

## Workflow

1. **Load the brief.** Read `.shape/<slug>.md` whole: what/why, the decisions made, the **reuse** notes, the `## design` block (components, data model, data flow — Large work; follow it), the `## behavior` map (happy path + edge→outcome — **build to this; it's the acceptance contract**), what's **out of scope** (a hard line — do not build it), and the `## tasks` slices.
2. **Reuse first.** Before writing anything, confirm the code/patterns named in the brief's reuse notes still exist, and prefer extending them over reinventing. If they've moved or changed, flag it and adjust rather than guessing.
3. **Implement every unchecked slice, in order.** Each slice is a thin end-to-end cut — build it as one. Stay inside scope; the out-of-scope bucket is a boundary, not a suggestion.
4. **Keep the gate green as you go.** Detect the project's checks in this order of authority: CLAUDE.md / docs → CI workflow files → `package.json` / `justfile` / `Makefile` / `pyproject.toml`. Run lint/format/typecheck/tests; fix before moving on. Run what CI runs, not a subset.
5. **Commit per slice, check the box.** Commit in logical units (conventional style; no AI attribution), and tick that slice's `- [ ]` → `- [x]` in the `## tasks` section as it lands — so progress is visible and a partial run is resumable.
6. **Safety valve.** If a slice reveals the idea was underspecified — surprises pile up, scope wants to grow, a decision the brief skipped now bites — STOP and hand back to `/ath:shape-idea` to re-shape. Don't improvise past the brief; that's the signal alignment was incomplete.
7. **Stop ready to ship.** Summarize what landed against the task list (done / skipped / blocked), then point to the next step: "to open the PR and green it: `/ath:ship`" — it loads this same brief as the intent. Building stops here; shipping is a separate step you invoke.
