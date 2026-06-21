# Draft-first — propose, then react to alignment

The move: don't ask the user to fill a blank. Read the one-liner, glance at the
codebase, and **write a draft brief with your decisions already made.** Hand them
something concrete to react to — people correct a proposal far faster, and more
accurately, than they answer open questions cold.

## What the draft must cover

Fill each of these in yourself, using your best read of the goal + the codebase.
Mark anything you're guessing so it's visibly a guess, not a fact.

- **Intent & value** — what we're building, who for, what changes once it ships.
  One sentence.
- **Scope edges** — what's explicitly OUT; the smallest version still worth shipping.
- **Decisions** — the forks (data model, naming, where the logic lives, sync vs
  async). Make the obvious calls; flag only the rest (see below).
- **Edge cases** — empty / zero / huge inputs; first run vs repeat; failure and
  rollback; migrating data that already exists. State how the draft handles each.
- **Done & proof** — what "done" looks like, and how we'll know it works (a test,
  a demo, a metric).
- **Constraints** — existing conventions, perf budget, dependencies, deadline,
  blast radius if it goes wrong.

## Surfacing the forks (the only thing you ask about)

A decision earns a question only when it **genuinely could go more than one way**
and the goal or codebase doesn't already settle it. Everything else: decide it,
note it, move on. That filter is what keeps this from becoming an interrogation.

For each real fork:

- Present **concrete options** — "card layout" vs "table", not "Option A / B".
- State **your lean and why**, so the user can rubber-stamp it in one word.
- Make it a clean either/or; offer "your call" when you truly have no preference.
- **Size the ask to the stakes:** cheap-to-reverse → lead with your pick and let
  them veto; expensive-to-undo → lay the options out and let them choose.

## How to drive it

- One **small batch** of forks at a time (3–5 max), never a wall.
- After each round, **revise the draft and show only what changed** — the diff,
  not the whole document again.
- **Reflect back:** "So we're building X, for Y, and NOT doing Z — right?"
  Alignment = the user confirms your restatement with no corrections.
- Stop when a restatement produces no changes. That converged draft *is* the
  single `.shape/<slug>.md` (brief + a `## tasks` section for the slices).
- Keep **deferred decisions visible** — anything handed back to you ("your call")
  gets noted, so it's not silently assumed.
- If a fork can't be settled without facts, go check (codebase → docs → web) and
  come back with the options, rather than guessing.
