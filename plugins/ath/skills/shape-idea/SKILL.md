---
name: shape-idea
description: Align on the idea before building — Claude develops a draft, then loops with you through the question tool on the gray areas, runs a consistency pass when they run dry, and ends by asking whether to adjust or build. Auto-sizes by complexity. Use when the user says "shape this", "let's plan", "think this through", "what should we build", "discuss before building", or starts a non-trivial feature or project. Do NOT use for tiny mechanical changes (just do them), for code-quality cleanups (use /ath:improve-code), or to find bugs (use /ath:ship-pr).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.5.0
---

# Shape

Reach a **shared understanding of the idea before any code**. The asset that matters is the alignment, not a document — you and the model converge on the *shape* of what you're building, then build fast against it.

> Replaces the old spec-driven flow. The point was never the spec; it was building context and discussing before building. This keeps that and drops the ceremony.

## Auto-size by complexity

- **Tiny** (≤3 files, one obvious change): skip shaping — just build it.
- **Medium** (a clear feature): the loop, light — a couple of gray areas, quick reuse scan, then the gate.
- **Large / fuzzy** (new domain, real ambiguity): the full loop — design sketch (reuse + components + data), slice into pieces, then the gate.

Always required: reach alignment and stop at a validated brief. Size is a running estimate, not locked at the start — if a "Tiny/Medium" task keeps surfacing gray areas mid-flow, re-size up and shape it properly.

## The loop

You bring the idea; Claude develops it, then loops with you through the **`AskUserQuestion` tool** until the picture is consistent and you sign off. Never interrogate from a blank page, and never decide silently — drive it through real questions.

1. **Develop the draft (draft-first).** Read the one-liner, look at the codebase, and write a short draft brief with your best-guess decisions filled in — what/why, scope edges, reuse, the decisions you can already make. For Large work, also sketch the *how* (next section) before slicing. Bring something concrete to react to.

2. **Highest-stakes fork first — ask before you anchor.** On the single decision most expensive to undo, ask the user how *they'd* call it *before* you reveal your own pick (an open `AskUserQuestion`). Anchoring is strongest on the choice that matters most — don't pre-frame that one. One fork only; everything else stays draft-first.

3. **Surface the gray areas as questions.** Everything else that genuinely could go more than one way → ask via `AskUserQuestion`, batched (the tool takes up to 4 at once), each as concrete options with your lean. Decide the obvious yourself; don't ask about what the codebase or goal already settles.

4. **Loop.** Fold each answer into the draft, re-surface anything new it opens, ask again. Keep going until a round surfaces no new gray areas.

5. **Consistency pass (when the gray areas run dry).** Make ONE pass over the whole brief for *material* internal contradictions — a decision that fights another, a task the scope excludes, an edge case nothing handles. Resolve what's clearly resolvable; raise the rest as gray areas (back to step 3). Material conflicts only — don't manufacture nitpicks, or the loop never closes.

6. **The exit gate.** When it's consistent, ask one `AskUserQuestion`: **adjust something, or ready to build?** Adjust → back into the loop. Ready → write/finalize `.shape/<slug>.md`, **stop**, and tell the user exactly what to run (see "Hand off").

Size the ask to the stakes: cheap-to-reverse decisions lead with your pick (the user vetoes if wrong); expensive-to-undo ones lay the options out and let them choose. Full playbook in `references/draft-first.md`.

## Sketch the "how" before slicing (auto-sized)

Part of develop (step 1) for Large work: sketch *how* you'll build it before turning it into tasks — draft-first, same as the brief. Keep it proportional and stop the moment you're writing more design than the feature warrants.

- **Reuse first** (even for Medium) — what existing code, patterns, or modules does this build on? Name them. The cheapest way to avoid reinventing something that already exists.
- **Components & data** (Large) — the key pieces and how they talk, plus the data model if there is one. A few bullets or mermaid lines, not a document.
- **The decisions that bite** — architectural forks go through the loop like any other gray area, so they're decided before they're baked into slices.

## Capture the alignment (lightweight, on disk)

Write a single `.shape/<slug>.md` — the converged draft itself: **what** we're building, **why**, the **decisions** made (including what to reuse), what's **out of scope** (including ideas parked for later, each marked *revisit*), and what's **still open**. Keep out-of-scope and open items as plain bullets — never checkboxes, so the task selector never mistakes them for work. Everything lives in one file so editing it later carries the full context; there's no separate write-up step, the draft you iterated *is* the brief. This is durable context (survives a context reset; a fresh session or the overnight loop reloads it), **not** a contract to satisfy line-by-line.

`<slug>` is a short kebab name for the idea. If `.shape/<slug>.md` already exists for a *different* idea, suffix it (`-2`) or ask — never silently overwrite another brief.

For Large work add a `## tasks` section to the same file — **vertical slices** (each a thin end-to-end cut that delivers something visible) as a GitHub-style checklist (`- [ ]`) the build side consumes.

## Don't fabricate

Before asserting how something works: check the codebase, then its docs, then the web; if you still don't know, **say so**. A wrong assumption here cascades into the build — and a draft full of confident guesses is worse than one that flags what it's unsure of. Uncertainty flagged beats confidence invented.

## Hand off — you invoke, the skill points the way

shape ends at a validated `.shape/<slug>.md` and does **not** build — shaping and execution stay separate. But don't leave the user guessing: when they pick "ready" at the gate, state the exact next step.

- **Daytime:** "Brief saved at `.shape/<slug>.md`. To build it: `/ath:implement-idea`, then `/ath:ship-pr` — both load this brief as the intent."
- **Overnight:** "Commit `.shape/<slug>.md`, then schedule `/ath:night-shift` — it builds one slice per run."

**Safety valve:** if building later reveals the idea was underspecified (surprises pile up), STOP and re-shape — that's the signal alignment was incomplete, not a license to improvise.

## Bundled Resources

### references/draft-first.md
The draft-first playbook — what a draft brief must cover, and how to surface the genuine forks as tool questions with a recommended pick instead of a wall of open prompts.
