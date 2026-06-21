---
name: shape
description: Align on the idea before building — Claude drafts a short brief with its best-guess decisions already filled in, surfaces only the forks that genuinely could go either way (each with a recommended pick), and revises against your reactions until you both hold the same picture. Auto-sizes by complexity. Use when the user says "shape this", "let's plan", "think this through", "what should we build", "discuss before building", or starts a non-trivial feature or project. Do NOT use for tiny mechanical changes (just do them), for code-quality cleanups (use /build:improve-code), or to find bugs (use /build:fix-pr).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.2.0
---

# Shape

Reach a **shared understanding of the idea before any code**. The asset that matters is the alignment, not a document — you and the model converge on the *shape* of what you're building, then build fast against it.

> Replaces the old spec-driven flow. The point was never the spec; it was building context and discussing before building. This keeps that and drops the ceremony.

## Auto-size by complexity

- **Tiny** (≤3 files, one obvious change): skip shaping — just build it.
- **Medium** (a clear feature): draft → react → a short BRIEF → build.
- **Large / fuzzy** (new domain, real ambiguity): draft → react → BRIEF → slice into buildable pieces → optional design notes.

Always required: reach alignment. Everything else scales to the work.

## The core move — draft first, then react

Do NOT interrogate from a blank page. Read the one-liner, take a quick look at the codebase, and **write a short draft brief with your best-guess decisions already filled in.** Then hand it back for reaction — the user edits a concrete proposal instead of answering open questions cold (full playbook in `references/draft-first.md`):

- **Lead with the draft** — what we're building, why, the scope edges, and the decisions you've already made.
- **Decide the obvious yourself; surface only the forks that bite.** When a decision genuinely could go more than one way, present it as concrete options with your lean and the reason — "leaning X because Y; the alternative is Z — keep or change?". If the call is settled by the codebase or the goal, just make it and note it.
- **The user reacts** — keeps the picks that fit, flips the ones that don't. Editing, not composing.
- **Revise and re-present only what changed.** Repeat until restating the idea produces no corrections — that convergence *is* the alignment.

Size the ask to the stakes: cheap-to-reverse decisions lead with your pick (veto if wrong); expensive-to-undo ones lay the options out and let the user choose.

## Capture the alignment (lightweight, on disk)

Write a single `.shape/<slug>.md` — the converged draft itself: **what** we're building, **why**, the **decisions** made, what we're **NOT** doing, and open questions. Everything lives in one file so editing it later carries the full context. There's no separate write-up step; the draft you iterated *is* the brief. This is durable context (survives a context reset; a fresh session or the overnight loop reloads it), **not** a contract to satisfy line-by-line. For Large work add a `## tasks` section to the same file — **vertical slices** (each a thin end-to-end cut that delivers something visible) as a GitHub-style checklist (`- [ ]`) the build side consumes.

## Don't fabricate

Before asserting how something works: check the codebase, then its docs, then the web; if you still don't know, **say so**. A wrong assumption here cascades into the build — and a draft full of confident guesses is worse than one that flags what it's unsure of. Uncertainty flagged beats confidence invented.

## Hand off to build

Shaping ends at alignment captured in `.shape/<slug>.md` (brief + slices). Building is `/build:open-pr` → `/build:fix-pr`, or the overnight loop (`/loops:night-shift`) reloads `.shape/<slug>.md` and builds one slice per run. **Safety valve:** if building reveals the idea was underspecified (surprises pile up), STOP and re-shape — that's the signal alignment was incomplete, not a license to improvise.

## Bundled Resources

### references/draft-first.md
The draft-first playbook — what a draft brief must cover, and how to surface only the genuine forks as recommended-pick choices instead of a wall of questions.
