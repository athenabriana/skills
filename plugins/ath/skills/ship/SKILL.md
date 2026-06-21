---
name: ship
description: Take the current branch to landed — your way. Quality-pass the diff, green the project's local checks, then land via the destination you choose: push to a feature branch, prepare a push to main, or open/finish a pull request. Reviews the diff for correctness bugs and simplification, runs the project's checks, and — on the PR path — triages review comments, pushes, and watches CI until green. Never merges and never pushes to a protected branch itself (it hands you that command). Use when the user says "ship it", "ship this", "land this branch", "push this to main", "push it to a branch", "open the PR", "finish the PR", or "green the PR". Do NOT use for triaging all open PRs and dependency updates (use /ath:maintain-repo), watching a PR on a loop (use /ath:watch-pr), or just summarizing the branch (use /ath:gather-branch-context).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.1.0
---

# Ship

Take the current branch all the way to landed — reviewed, checks green, committed — then land it the way you pick: push to a branch, prepare a push to main, or open and green a PR. The quality pass is the same regardless of destination; only the landing differs. **Never merges, and never pushes to a protected branch itself** — landing on `main`/`master`/`release` stays a human action (your guard reserves it), so ship preps everything and hands you the command.

## Prerequisites

- For the PR path: `gh` authenticated (`gh auth status`, repo + workflow scopes). If not, instruct the user to run `gh auth login`.
- Resolve the current branch's PR up front: `gh pr view --json number,url,title,baseRefName`. If one exists, it's the default destination ("finish the PR").

## Step 1 — Pick the destination

Ask one `AskUserQuestion` with the three landings (lead with the one that fits the current state — "finish the PR" if a PR already exists, else "open a PR"):

- **Open / finish a PR** — full flow: create the PR if none exists, triage review comments, push, watch CI until green.
- **Push to a feature branch** — commit and push to a non-protected branch (the current one, or a new name you give). No PR. Reversible, so ship runs it.
- **Push to main (or another protected branch)** — ship does the whole quality pass and commits, then **hands you the exact push command** and stops. Your guard reserves protected-branch landing for a human; ship never runs it.

## Step 2 — Quality pass + green the gate (always, every destination)

This runs identically whatever the destination — it's the substance of shipping. Self-contained; do not invoke other skills. Review criteria live in `references/review-checklist.md`.

Launch the read-only work concurrently — review agents in one message, scripts/checks as background Bash:

1. **Review agents** (Agent tool, read-only — they report, never edit). Each gets the diff scope (`git diff <base>...HEAD`), the path to `references/review-checklist.md`, and ONE lens:
   - `logic-edges` — logic errors, edge cases, error handling
   - `async-state` — async/concurrency, state & lifecycle
   - `contracts-security` — contract breaks, security, type safety
   - `quality` — the entire Pass 2 (reuse, simplification, dead weight, efficiency, altitude, consistency)

   Each verifies every finding against the actual file (not just the diff) and returns: `file:line | what | evidence | suggested fix | confidence`.
   For tiny diffs (≲2 files / ≲100 lines), skip the fan-out and apply the checklist in the main context.
   If a `.shape/*.md` brief matches this branch, pass it to the agents as the intended scope — review the diff against what was agreed (did it build the shaped thing, and only that?), not just generic correctness. Its `## behavior` map is the acceptance contract: each `WHEN … THEN …` row is a test — check the happy path is built and each mapped edge is handled per its outcome. A mapped behavior with no corresponding code or test is a finding.

2. **Local checks** (background): detect the project's check commands in this order of authority: project CLAUDE.md / docs, CI workflow files (`.github/workflows/`), then `package.json` / `justfile` / `Makefile` / `pyproject.toml`. Run the full gate CI runs — lint, format, typecheck, tests — as concurrent background shells.

3. **Apply fixes in the main context only** (agents never edit — single writer): dedupe review findings against each other, re-check each against the file, then apply high-confidence review fixes + local-check fixes. Quality edits change zero behavior and touch only code this branch changed. Keep uncertain findings for the summary.

4. **Re-run the local gate** (failed/affected first, then the full gate) until clean.

5. **Commit** in logical units (conventional style; no AI attribution).

Now land it per the Step 1 choice.

## Land it → Push to a feature branch

1. Confirm the target branch — the current one, or a new name the user gave.
2. Push: `git push -u origin <branch>`.
3. Report what landed (commits, files, gate result). No PR is opened — if they want one later, ship again with the PR destination or use `/ath:watch-pr`.

## Land it → Push to main (or another protected branch)

Everything is committed and the gate is green. Ship stops here and hands off — your guard (and good practice) reserves protected-branch landing for a human.

1. Show the summary: commits, files, gate result.
2. Hand off the exact command, e.g. `git push origin HEAD:main` (or `git -C <repo> push origin <branch>`).
3. Note that CI will run on push; if it's worth watching, suggest `/ath:watch-pr` after.

## Land it → Open / finish a PR

### Create the PR (only if none exists)

1. Gather context: `python scripts/gather_pr_context.py` → JSON with `branch`, `upstream`, `base_branch`, `commit_log`, `diff_stat`, `uncommitted_changes`, `pr_template`.
2. If the branch has no upstream, note that `gh pr create` pushes automatically.
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
   Add `--base`, `--draft`, `--label`, `--reviewer`, `--assignee` as requested. Output the PR URL.

### Triage comments → approval gate → push → reply

1. **Fetch comments** (background): `python scripts/fetch_comments.py` — conversation comments, reviews, and review threads (with `id` and `isResolved`) as JSON.
2. **Triage** each **unresolved** thread: **fix** (implement it), **answer** (draft a short reply, no code change), or **unclear** (needs the user's call). Apply **fix**-thread code changes in the main context, re-run the gate, build the triage table: `# | file:line | comment summary | verdict | planned action/reply`.
3. **Approval gate** — show the triage table + summary of all local changes. **Wait for approval.** Then:
   - Commit any new units and push.
   - **fix** threads: reply with what was done + the commit sha, then resolve — `python scripts/reply_resolve_thread.py --thread-id <id> --body "Fixed in <sha>: <one-liner>"`
   - **answer** threads: reply but do NOT resolve (the reviewer closes it) — `python scripts/reply_resolve_thread.py --thread-id <id> --body "..." --no-resolve`

### Watch CI until green

1. `gh pr checks <pr> --watch --interval 30` (or poll `python scripts/inspect_pr_checks.py --repo "." --pr <number> --json`).
2. All green → final summary, done.
3. Non-GitHub-Actions checks (Buildkite, CircleCI, …): report the details URL, don't debug.

### On CI failure: diagnose before editing

Read the actual failure logs before touching any source file (multiple failures → fetch all logs concurrently):
- `python scripts/inspect_pr_checks.py --repo "." --pr <number>` (run IDs + failure snippets), or `gh run view <run_id> --log-failed`.
Identify the root cause with a specific log snippet, then fix → commit → push → watch again. Guessing wastes a 5-20 min CI cycle.

**Loop limit:** after 3 failed fix cycles, stop and report the diagnosis of each attempt.

## Bundled Resources

### references/review-checklist.md
Two-pass diff review checklist for the quality pass: correctness (bug-finding) and quality (simplification) criteria.

### scripts/gather_pr_context.py
Collect branch, upstream, base, commit log, diff stat, uncommitted changes, and PR template in one call (PR creation). Prints JSON.

### scripts/fetch_comments.py
Fetch all PR conversation comments, reviews, and review threads (with thread IDs and resolved state) via `gh api graphql`. Prints JSON.

### scripts/reply_resolve_thread.py
Reply to a review thread and/or resolve it. `--thread-id` from fetch_comments.py; `--body` for the reply; `--no-resolve` to reply without resolving.

### scripts/inspect_pr_checks.py
Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero while failures remain.
