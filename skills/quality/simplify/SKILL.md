---
name: quality-simplify
description: Review the code this branch changed for reuse, simplification, dead weight, efficiency, altitude, and consistency, then apply the cleanups — quality only, behavior-preserving, scoped strictly to code the branch already touched, re-running local checks after each edit. Use when the user says "simplify", "simplify the diff", "clean this up", "tidy this code", "reduce complexity", or "refactor for clarity". Do NOT use to find bugs (that is correctness review — use /gh-fix-pr), to open a PR (use /gh-open-pr), or to touch code this branch did not change.
license: Apache-2.0
metadata:
  author: adapted from Claude Code's /simplify (Anthropic) by Athena Freitas - github.com/athenacfr
  version: 1.0.0
---

# Simplify

A focused quality pass over the current change: make it simpler, leaner, and more
consistent **without changing behavior**. This is the standalone version of
`gh-fix-pr`'s Pass 2 — reach for it any time, not just when finalizing a PR.

**Quality only.** It does not hunt for bugs. If you want correctness review, that
is Pass 1 of `/gh-fix-pr` — use that skill. Mixing the two makes both passes worse.

> **Name collision:** Claude Code ships a built-in `/simplify`. This repo skill is
> installed as `quality-simplify` (group-prefixed, per the repo naming convention)
> precisely so it does not shadow — or get shadowed by — the built-in. They serve
> the same intent; this is the repo-native version aligned with `gh-fix-pr` Pass 2.

## Scope (read before editing)

- **Only touch code this branch already changed.** Never refactor untouched code
  "while at it" — that turns a clean diff into an unreviewable one.
- **Zero behavior change.** Every edit must be behavior-preserving: same inputs,
  same outputs, same side effects. A "simplification" that changes what the code
  does is a regression, not a cleanup.
- **Clarity over brevity.** Explicit, readable code beats clever or compact code.
  Do not trade "fewer lines" for legibility — collapsing logic into a dense
  one-liner or a nested ternary is not a simplification.

## Workflow

1. **Get the change scope.** Resolve the base (default branch) and read the diff —
   `git diff <base>...HEAD` plus any uncommitted changes (`git diff`). Read each
   hunk **with its surrounding file context** (open the file, not just the diff)
   before judging it — a simplification needs the whole picture.
2. **Review against the checklist** in `references/quality-checklist.md` (reuse,
   simplification, dead weight, efficiency, altitude, consistency). Before
   concluding a helper doesn't exist, **search the codebase** — duplication you
   can't see isn't reuse you can claim.
3. **Apply the cleanups** to the working tree, scoped to changed code only. Match
   the surrounding code's naming, error envelopes, and patterns. For a large diff,
   fan out read-only review sub-agents (one per checklist area) that return
   `file:line | what | suggested fix | confidence`, then apply from the deduped
   findings in a single writer pass (no conflicting edits).
4. **Re-run the local gate** for the touched area (lint / format / typecheck /
   tests) — a cleanup that breaks a check is not done. Reuse the project's check
   commands (CLAUDE.md / CI workflows / package scripts).
5. **Summarize** what changed and why, grouped by checklist area, and flag any
   cleanup you held back as too risky to do silently.

## Maintain balance — do NOT over-simplify

Stop short of changes that hurt the code even if they shrink it:

- Don't fold separate concerns into one function/component to save a definition.
- Don't strip a helpful abstraction that genuinely organizes the code.
- Don't make the code harder to debug, extend, or read in pursuit of "elegance".
- When an edit's value is marginal and its risk to clarity is real, leave it.

## Anti-Patterns (DO NOT)

- **DO NOT** change behavior — if you're unsure an edit is behavior-preserving,
  leave it and flag it instead.
- **DO NOT** touch code outside this branch's diff.
- **DO NOT** report or "fix" bugs here — that's correctness review (`/gh-fix-pr`).
- **DO NOT** introduce nested ternaries or dense one-liners "to simplify".
- **DO NOT** claim a helper already exists without searching for it first.
- **DO NOT** skip the re-run of local checks after editing.

## Bundled Resources

### references/quality-checklist.md
The six quality criteria applied here — the canonical simplification checklist,
kept consistent with `gh-fix-pr` Pass 2 so the standalone and PR-finalization
flows judge a diff the same way.
