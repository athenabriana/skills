---
name: ship-pr
description: Ship the current branch as a pull request, end-to-end — create the PR if none exists yet, then take it to ready-to-merge. Drafts title/body and opens the PR (skips this if one already exists), reviews the diff for correctness bugs and simplification, runs the project's local checks, triages review comments (fixes what makes sense, replies and resolves threads), pushes, and watches CI until green — diagnosing failures from real logs. Use when the user says "ship it", "ship the PR", "open and green the PR", "create the PR and finish it", "fix PR", "green the PR", or "leave the PR ready". Do NOT use for triaging all open PRs and dependency updates (use /ath:maintain-repo), watching a PR on a loop (use /ath:watch-pr), or just summarizing the branch (use /ath:gather-branch-context).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.0.0
---

# Ship PR

Take the current branch all the way to a green, ready-to-merge PR: open it if needed, then quality pass, local checks, review comments handled, CI green. Never merges — landing stays human.

## Prerequisites

Ensure `gh` is authenticated: `gh auth status` (repo + workflow scopes required). If not, instruct the user to run `gh auth login`.

Resolve the current branch's PR: `gh pr view --json number,url,title,baseRefName`.
- **PR exists** → skip Phase 0, go to Phase 1.
- **No PR** → do Phase 0 first.

## Phase 0 — Create the PR (only if none exists)

1. Gather context: `python scripts/gather_pr_context.py` → JSON with `branch`, `upstream`, `base_branch`, `commit_log`, `diff_stat`, `uncommitted_changes`, `pr_template`.
2. If there are uncommitted changes, ask whether to commit them first. If the branch has no upstream, note that `gh pr create` pushes automatically.
3. Draft from the commits + diff (and a matching `.shape/*.md` brief if present — it's the intended scope):
   - **Title**: conventional commit style `<type>(<scope>): <description>` (≤70 chars).
   - **Body**: follow `.github/pull_request_template.md` if it exists (fill every section; mark N/A where not applicable). Otherwise: Context (why) → Changes (grouped by purpose, not file) → Breaking Changes (only if any).
4. Present title + body, get approval/edits, then create:
   ```
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   <body>
   EOF
   )"
   ```
   Add `--base`, `--draft`, `--label`, `--reviewer`, `--assignee` as requested. Output the PR URL, then continue to Phase 1.

## Finalize — collect → adjust

Phase 1 gathers every input in parallel; Phase 2 applies all fixes from the complete picture. Both are local and run without asking. Phase 3 is ONE approval gate covering everything outward-facing (push + thread replies). Phases 4-5 run autonomously until CI is green.

### Phase 1 — Collect (read-only, all in parallel)

Self-contained — do not invoke other skills. Review criteria live in `references/review-checklist.md`.

Launch ALL concurrently — review agents in a single message, scripts/checks as background Bash:

1. **Review agents** (Agent tool, read-only — they report, never edit). Each gets the diff scope (`git diff <base>...HEAD`), the path to `references/review-checklist.md`, and ONE lens:
   - `logic-edges` — logic errors, edge cases, error handling
   - `async-state` — async/concurrency, state & lifecycle
   - `contracts-security` — contract breaks, security, type safety
   - `quality` — the entire Pass 2 (reuse, simplification, dead weight, efficiency, altitude, consistency)

   Each verifies every finding against the actual file (not just the diff) and returns: `file:line | what | evidence | suggested fix | confidence`.
   For tiny diffs (≲2 files / ≲100 lines), skip the fan-out and apply the checklist in the main context.
   If a `.shape/*.md` brief matches this branch, pass it to the agents as the intended scope — review the diff against what was agreed (did it build the shaped thing, and only that?), not just generic correctness.

2. **Comments fetch** (background): `python scripts/fetch_comments.py` — conversation comments, reviews, and review threads (with `id` and `isResolved`) as JSON.
3. **Local checks** (background): detect the project's check commands in this order of authority: project CLAUDE.md / docs, CI workflow files (`.github/workflows/`), then `package.json` / `justfile` / `Makefile` / `pyproject.toml`. Run the full gate CI runs — lint, format, typecheck, tests — as concurrent background shells. A baseline run that surfaces pre-existing failures while the review agents work.

### Phase 2 — Adjust (triage, apply fixes, green local checks)

1. **Triage** each **unresolved** thread: **fix** (implement it), **answer** (draft a short reply, no code change), or **unclear** (needs the user's call).
2. **Apply in the main context only** (agents never edit — single writer): dedupe review findings against each other and the comment fixes, re-check each against the file, then apply high-confidence review fixes + **fix**-thread changes + baseline-check fixes. Quality edits change zero behavior and touch only code this branch changed. Keep uncertain findings for the Phase 3 summary.
3. **Re-run the local gate** (failed/affected first, then the full gate) until clean.
4. Build the triage table: `# | file:line | comment summary | verdict | planned action/reply`.

### Phase 3 — Approval gate, then commit, push & reply

1. Show the user: triage table + summary of all local changes. **Wait for approval.**
2. After approval:
   - Commit in logical units and push.
   - **fix** threads: reply with what was done + the commit sha, then resolve — `python scripts/reply_resolve_thread.py --thread-id <id> --body "Fixed in <sha>: <one-liner>"`
   - **answer** threads: reply but do NOT resolve (the reviewer closes it) — `python scripts/reply_resolve_thread.py --thread-id <id> --body "..." --no-resolve`

### Phase 4 — Watch CI until green

1. `gh pr checks <pr> --watch --interval 30` (or poll `python scripts/inspect_pr_checks.py --repo "." --pr <number> --json`).
2. All green → final summary, done.
3. Non-GitHub-Actions checks (Buildkite, CircleCI, …): report the details URL, don't debug.

### Phase 5 — On CI failure: diagnose before editing

Read the actual failure logs before touching any source file (multiple failures → fetch all logs concurrently):
- `python scripts/inspect_pr_checks.py --repo "." --pr <number>` (run IDs + failure snippets), or `gh run view <run_id> --log-failed`.
Identify the root cause with a specific log snippet, then fix → commit → push → back to Phase 4. Guessing wastes a 5-20 min CI cycle.

**Loop limit:** after 3 failed fix cycles, stop and report the diagnosis of each attempt.

## Bundled Resources

### references/review-checklist.md
Two-pass diff review checklist for Phase 1: correctness (bug-finding) and quality (simplification) criteria.

### scripts/gather_pr_context.py
Collect branch, upstream, base, commit log, diff stat, uncommitted changes, and PR template in one call (Phase 0). Prints JSON.

### scripts/fetch_comments.py
Fetch all PR conversation comments, reviews, and review threads (with thread IDs and resolved state) via `gh api graphql`. Prints JSON.

### scripts/reply_resolve_thread.py
Reply to a review thread and/or resolve it. `--thread-id` from fetch_comments.py; `--body` for the reply; `--no-resolve` to reply without resolving.

### scripts/inspect_pr_checks.py
Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero while failures remain.
