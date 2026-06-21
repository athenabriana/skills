---
name: shape
description: Align on the idea before building — Claude drafts a short brief with its best-guess decisions already filled in, surfaces only the forks that genuinely could go either way (each with a recommended pick), and revises against your reactions until you both hold the same picture. Auto-sizes by complexity. Use when the user says "shape this", "let's plan", "think this through", "what should we build", "discuss before building", or starts a non-trivial feature or project. Do NOT use for tiny mechanical changes (just do them), for code-quality cleanups (use /build:improve-code), or to find bugs (use /build:fix-pr).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.4.0
---

# Shape

Reach a **shared understanding of the idea before any code**. The asset that matters is the alignment, not a document — you and the model converge on the *shape* of what you're building, then build fast against it.

> Replaces the old spec-driven flow. The point was never the spec; it was building context and discussing before building. This keeps that and drops the ceremony.

## Auto-size by complexity

- **Tiny** (≤3 files, one obvious change): skip shaping — just build it.
- **Medium** (a clear feature): draft → react → quick reuse scan → BRIEF → you validate.
- **Large / fuzzy** (new domain, real ambiguity): draft → react → design sketch (reuse + components + data) → BRIEF → slice → you validate.

Always required: reach alignment and stop at a validated brief. Size is a running estimate, not locked at the start — if a "Tiny/Medium" task keeps surfacing forks mid-flow, re-size up and shape it properly.

## The core move — draft first, then react

Do NOT interrogate from a blank page. Read the one-liner, take a quick look at the codebase, and **write a short draft brief with your best-guess decisions already filled in.** Then hand it back for reaction — the user edits a concrete proposal instead of answering open questions cold (full playbook in `references/draft-first.md`):

- **Ask first on the single highest-stakes fork.** Before you reveal your pick on the one decision that's most expensive to undo, ask how *they'd* call it — anchoring is strongest on the choice that matters most, so don't pre-frame that one. One question, the biggest fork only; everything else stays draft-first.
- **Lead with the draft** — what we're building, why, the scope edges, and the decisions you've already made.
- **Decide the obvious yourself; surface only the forks that bite.** When a decision genuinely could go more than one way, present it as concrete options with your lean and the reason — "leaning X because Y; the alternative is Z — keep or change?". If the call is settled by the codebase or the goal, just make it and note it.
- **The user reacts** — keeps the picks that fit, flips the ones that don't. Editing, not composing.
- **Revise and re-present only what changed.** Keep going until the user actively validates the brief — not until they merely stop objecting. Silence is disengagement, not agreement.

Size the ask to the stakes: cheap-to-reverse decisions lead with your pick (veto if wrong); expensive-to-undo ones lay the options out and let the user choose.

## Sketch the "how" before slicing (auto-sized)

Once you both hold the *what*, sketch *how* you'll build it before turning it into tasks — draft-first, same as the brief. Keep it proportional and stop the moment you're writing more design than the feature warrants.

- **Reuse first** (even for Medium) — what existing code, patterns, or modules does this build on? Name them. The cheapest way to avoid reinventing something that already exists.
- **Components & data** (Large) — the key pieces and how they talk, plus the data model if there is one. A few bullets or mermaid lines, not a document.
- **The decisions that bite** — surface architectural forks the same draft-first way (your lean + the alternative), so they're decided before they're baked into slices.

## Capture the alignment (lightweight, on disk)

Write a single `.shape/<slug>.md` — the converged draft itself: **what** we're building, **why**, the **decisions** made (including what to reuse), what's **out of scope** (including ideas parked for later, each marked *revisit*), and what's **still open**. Keep out-of-scope and open items as plain bullets — never checkboxes, so the task selector never mistakes them for work. Everything lives in one file so editing it later carries the full context; there's no separate write-up step, the draft you iterated *is* the brief. This is durable context (survives a context reset; a fresh session or the overnight loop reloads it), **not** a contract to satisfy line-by-line.

`<slug>` is a short kebab name for the idea. If `.shape/<slug>.md` already exists for a *different* idea, suffix it (`-2`) or ask — never silently overwrite another brief.

For Large work add a `## tasks` section to the same file — **vertical slices** (each a thin end-to-end cut that delivers something visible) as a GitHub-style checklist (`- [ ]`) the build side consumes.

## Don't fabricate

Before asserting how something works: check the codebase, then its docs, then the web; if you still don't know, **say so**. A wrong assumption here cascades into the build — and a draft full of confident guesses is worse than one that flags what it's unsure of. Uncertainty flagged beats confidence invented.

## Stop at the brief — validate before building

Shaping **ends at a written, validated `.shape/<slug>.md`**. Do not start building, do not open a PR, do not chain into another skill. Write the brief, present it, and **wait for the user to validate** — they read it and either approve or send corrections. That explicit approval is the alignment gate: silence is not approval, and an unread brief is not a validated one.

Only after validation does building happen, as a **separate, user-initiated step**: `/build:open-pr` → `/build:fix-pr` (which load this brief as the intent behind the work), or the overnight loop (`/loops:night-shift`) reloads `.shape/<slug>.md` and builds one slice per run. **Safety valve:** if building later reveals the idea was underspecified (surprises pile up), STOP and re-shape — that's the signal alignment was incomplete, not a license to improvise.

## Bundled Resources

### references/draft-first.md
The draft-first playbook — what a draft brief must cover, and how to surface only the genuine forks as recommended-pick choices instead of a wall of questions.
