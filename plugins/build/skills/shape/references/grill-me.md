# Grill-me — interrogate to alignment

The move: instead of asking the user to write a spec, ask them the questions that
surface the real shape of what they want. Drive until there are no surprises left.
The goal is a shared picture, not a filled-in template.

## Question categories (pull what fits — don't ask all of them)

- **Intent & value** — What are we building? Who is it for? What changes for them
  once it ships? Give me the one-sentence version.
- **Scope edges** — What's explicitly OUT? What's the smallest version still worth
  shipping? What are we deliberately NOT solving now?
- **Decisions that bite** — Where are the forks (data model, naming, where the
  logic lives, sync vs async)? Decide now or defer *explicitly*. What existing
  pattern should this follow?
- **Edge cases** — empty / zero / huge inputs; first run vs repeat; concurrent
  use; failure and rollback; migrating data that already exists.
- **Done & proof** — What does "done" look like? How do we know it works (a test,
  a demo, a metric)? What would make you reject it in review?
- **Constraints** — existing conventions, perf budget, dependencies, deadline,
  blast radius if it goes wrong.

## How to drive it

- Ask in **small batches** (3–5), not a wall of 40 at once.
- Once the shape emerges, prefer concrete either/or questions over open ones.
- **Reflect back:** "So we're building X, for Y, and NOT doing Z — right?"
  Alignment = the user confirms your restatement with no corrections.
- Stop when a restatement produces no changes. Capture that as `BRIEF.md`.
- Make the **deferred decisions visible** — note anything the user handed to you
  ("your call") so it's not silently assumed.
- If a question can't be answered without facts, go check (codebase → docs → web)
  rather than guessing — then come back with the options.
