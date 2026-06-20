---
name: shape
description: Align on the idea before building — Claude interrogates you and you discuss until you both hold the same picture of what to build, then capture a lightweight brief and slice it into buildable pieces. Auto-sizes by complexity. Use when the user says "shape this", "let's plan", "think this through", "what should we build", "discuss before building", or starts a non-trivial feature or project. Do NOT use for tiny mechanical changes (just do them), for code-quality cleanups (use /improve-code), or to find bugs (use /gh-fix-pr).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.0.0
---

# Shape

Reach a **shared understanding of the idea before any code**. The asset that matters is the alignment, not a document — you and the model converge on the *shape* of what you're building, then build fast against it.

> Replaces the old spec-driven flow. The point was never the spec; it was building context and discussing before building. This keeps that and drops the ceremony.

## Auto-size by complexity

- **Tiny** (≤3 files, one obvious change): skip shaping — just build it.
- **Medium** (a clear feature): grill-me → a short BRIEF → build.
- **Large / fuzzy** (new domain, real ambiguity): grill-me → BRIEF → slice into buildable pieces → optional design notes.

Always required: reach alignment. Everything else scales to the work.

## The core move — grill-me (Claude interrogates you)

Do NOT ask the user to write a spec. **Ask them the sharp questions** until you both hold the same picture (full playbook in `references/grill-me.md`):

- What are we building, and **why** — what changes for the user?
- What's explicitly **out of scope** / the smallest version still worth shipping?
- The **decisions that bite later** (data model, where logic lives, naming) — decide now or defer explicitly.
- The **edge cases** that matter (empty/huge inputs, first-run vs repeat, failure/rollback, migration).
- What does **"done"** look like, and how do we know it works?
- **Constraints:** existing patterns, perf, deps, deadline, blast radius.

Ask in small batches, reflect back ("so we're building X for Y, NOT doing Z — right?"), and keep going until restating the idea produces no more corrections. That confirmation *is* the alignment.

## Capture the alignment (lightweight, on disk)

Write `.shape/<slug>/BRIEF.md` — **what** we're building, **why**, the **decisions** made, what we're **NOT** doing, and open questions. This is durable context (survives a context reset; a fresh session or the overnight loop reloads it), **not** a contract to satisfy line-by-line. For Large work also write `.shape/<slug>/tasks.md` — **vertical slices** (each a thin end-to-end cut that delivers something visible), as a checklist the build side consumes.

## Don't fabricate

Before asserting how something works: check the codebase, then its docs, then the web; if you still don't know, **say so**. A wrong assumption here cascades into the build — uncertainty flagged beats confidence invented.

## Hand off to build

Shaping ends at alignment + BRIEF (+ slices). Building is `/gh-open-pr` → `/gh-fix-pr`, or the overnight loop (`/night-shift`) reloads `.shape/<slug>/tasks.md` and builds one slice per run. **Safety valve:** if building reveals the idea was underspecified (surprises pile up), STOP and re-shape — that's the signal alignment was incomplete, not a license to improvise.

## Bundled Resources

### references/grill-me.md
The interrogation playbook — question categories and how to drive to alignment without writing a spec first.
