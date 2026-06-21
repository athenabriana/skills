---
name: shape-idea
description: Align on the idea before building — Claude develops a draft, loops with you through the question tool on the gray areas (the load-bearing technical decisions AND a meticulous behavior map: happy path + edge cases with expected outcomes), runs a completeness + consistency pass, and gates on adjust-or-build, blocking while any load-bearing decision or behavior is still open. Auto-sizes by complexity. Use when the user says "shape this", "let's plan", "think this through", "what should we build", "discuss before building", or starts a non-trivial feature or project. Do NOT use for tiny mechanical changes (just do them), for code-quality cleanups (use /ath:improve-code), or to find bugs (use /ath:ship-pr).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.8.0
---

# Shape

Reach a **shared understanding of the idea before any code**. The asset that matters is the alignment, not a document — you and the model converge on the *shape* of what you're building, then build fast against it.

> Replaces the old spec-driven flow. The point was never the spec; it was building context and discussing before building. This keeps that and drops the ceremony.

## Auto-size by complexity

- **Tiny** (≤3 files, one obvious change): skip shaping — just build it.
- **Medium** (a clear feature): the loop — gray areas + reuse scan + the load-bearing technical forks + the behavior map (happy path + edges), then the gate.
- **Large / fuzzy** (new domain, real ambiguity): the full loop — reuse + components + data-flow design, the technical forks, the behavior map, slice into pieces, then the gate.

Always required: reach alignment, **close the load-bearing technical decisions, map the behavior**, and stop at a validated brief. Size is a running estimate, not locked at the start — if a "Tiny/Medium" task keeps surfacing gray areas mid-flow, re-size up and shape it properly.

## The loop

You bring the idea; Claude develops it, then loops with you through the **`AskUserQuestion` tool** until the picture is consistent and you sign off. Never interrogate from a blank page, and never decide silently — drive it through real questions.

1. **Develop the draft (draft-first).** Read the one-liner, look at the codebase, and write a short draft brief with your best-guess decisions filled in — what/why, scope edges, reuse, the decisions you can already make. For Large work, also sketch the *how* (next section) before slicing. Bring something concrete to react to.

2. **Highest-stakes fork first — ask before you anchor.** On the single decision most expensive to undo, ask the user how *they'd* call it *before* you reveal your own pick (an open `AskUserQuestion`). Anchoring is strongest on the choice that matters most — don't pre-frame that one. One fork only; everything else stays draft-first.

3. **Surface the gray areas as questions.** Everything else that genuinely could go more than one way → ask via `AskUserQuestion`, batched (the tool takes up to 4 at once), each as concrete options with your lean. Decide the obvious yourself; don't ask about what the codebase or goal already settles.

4. **Loop.** Fold each answer into the draft, re-surface anything new it opens, ask again. Keep going until a round surfaces no new gray areas.

5. **Completeness + consistency pass (when the gray areas run dry).** Make ONE pass over the whole brief for: (a) **unresolved load-bearing decisions** — a technical fork building can't proceed without (data model, contract/interface, where logic lives, error/edge handling, integration points) still blank or "TBD"; (b) **unmapped or unanswered behavior** — a happy-path step glossed over, or an edge case with no decided outcome; and (c) **material contradictions** — a decision that fights another, a task the scope excludes, an edge case nothing handles. Anything found goes back to step 3 as a gray area. Load-bearing gaps, behavior holes, and real conflicts only — don't manufacture nitpicks, or the loop never closes.

6. **The exit gate — blocks on open load-bearing decisions.** First list what's **still open** (unresolved load-bearing decisions + parked questions). Then ask one `AskUserQuestion`:
   - **If any load-bearing decision is still open:** do NOT offer a clean "build". The only options are **resolve it now** or **defer explicitly** ("decide at build time" — recorded as such in the brief). Never a silent "build anyway".
   - **If nothing load-bearing is open:** *adjust something, or ready to build?* Adjust → back into the loop. Ready → write/finalize `.shape/<slug>.md`, **stop**, and tell the user exactly what to run (see "Hand off").

Size the ask to the stakes: cheap-to-reverse decisions lead with your pick (the user vetoes if wrong); expensive-to-undo ones lay the options out and let them choose. Full playbook in `references/draft-first.md`.

## Decide the technical forks (required for Medium+)

Before the gate, the load-bearing technical decisions must be **made or explicitly deferred** — not left implicit. This is the substance the old Design phase carried; surface each that genuinely could go more than one way as a tool question (draft-first: your lean + the alternatives). Skip only what the codebase or goal already settles. Don't write a design document — close the decisions.

- **Reuse** — what existing code, patterns, or modules this builds on. Name them (the cheapest guard against reinventing).
- **Data model / shape** — the entities, fields, and relationships, or the shape of the data flowing through.
- **Contracts & interfaces** — the function/API/CLI signatures and the boundaries between the pieces.
- **Where the logic lives** — which component/layer owns what, and how the pieces talk (a few bullets or mermaid lines for Large work, not a document).
- **Error & edge handling** — for each edge in the behavior map (below), decide *how* it's handled (failure & rollback, validation, retries). Map the case in the behavior; decide the handling here.
- **Integration points** — what it touches: existing systems, dependencies, external services.

These are the decisions that bite *after* you've built against them — expensive to undo — so they get closed here, before slicing. A fork left open is what the gate blocks on. For Large work, record the closed decisions in the brief's `## design` section; for Medium, inline in the decisions.

## Map the behavior (required for Medium+)

The behaviors are what guarantee the built thing matches the idea — so map them **meticulously, not as a sketch**. An unmapped behavior is an unverified assumption about the final result; the completeness of this map is the fidelity between idea and outcome.

- **Happy path** — walk the main flow step by step and concretely: input → what happens → observable output. Don't abbreviate; the steps you skip are the gaps that surface in review.
- **Edge cases** — every meaningful deviation, each with its **expected outcome**: empty / zero / huge input, invalid input, first-run vs repeat, concurrent use, failure & rollback, denied permission/auth, partial or interrupted runs, migrating existing data. Map the *outcome*, not just that the case exists.

Walking each behavior surfaces decisions you haven't made — those go back into the loop as gray areas, and each edge's outcome drives its handling in the technical forks. **A behavior with no decided outcome is an open item the gate blocks on.** This map doubles as the acceptance criteria: each behavior is something `/ath:ship-pr` and the local gate check against, and each happy-path segment is a vertical slice. Record it in a `## behavior` section for Large work (happy path + an edge→outcome table); inline for Medium.

## Capture the alignment (lightweight, on disk)

Write a single `.shape/<slug>.md` — the converged draft itself: **what** we're building, **why**, the **decisions** made (including what to reuse), what's **out of scope** (including ideas parked for later, each marked *revisit*), and what's **still open**. Keep out-of-scope and open items as plain bullets — never checkboxes, so the task selector never mistakes them for work. Everything lives in one file so editing it later carries the full context; there's no separate write-up step, the draft you iterated *is* the brief. This is durable context (survives a context reset; a fresh session or the overnight loop reloads it), **not** a contract to satisfy line-by-line.

`<slug>` is a short kebab name for the idea. If `.shape/<slug>.md` already exists for a *different* idea, suffix it (`-2`) or ask — never silently overwrite another brief.

For **Large** work, capture the closed technical decisions in a `## design` section — components and their boundaries, the data model, key data flows, and the decisions that bite — so the architecture is reviewable as one block and the build side (`/ath:implement-idea`, `/ath:night-shift`) reads it as the intent. **Medium** work keeps these inline in the decisions above; no `## design` block (that would be ceremony for a small feature).

For Large work, also capture the **behavior map** in a `## behavior` section — the happy path step by step plus an edge→expected-outcome table. It's the acceptance contract the build and review check against (Medium keeps it inline).

Also for Large work, add a `## tasks` section to the same file — **vertical slices** (each a thin end-to-end cut that delivers something visible) as a GitHub-style checklist (`- [ ]`) the build side consumes.

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
