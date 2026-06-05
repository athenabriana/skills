---
name: gh-fix-pr
description: Finalize and green the open GitHub PR for the current branch, end-to-end. Reviews the diff for correctness bugs and simplification opportunities, runs the project's local checks (lint, typecheck, tests), triages review comments (fixes what makes sense, replies and resolves threads), pushes, then watches CI until green — diagnosing failures from actual logs. Use when user says "fix PR", "finish the PR", "green the PR", "leave the PR ready", or "address comments and fix CI". Do NOT use for creating PRs (use /gh-open-pr).
license: MIT
metadata:
  author: Athena Freitas - github.com/athenacfr
  version: 2.0.0
---

# Fix PR

Take the open PR for the current branch from "code pushed" to "ready to merge": quality pass, local checks, review comments handled, CI green.

## Prerequisites

Ensure `gh` is authenticated: `gh auth status` (repo + workflow scopes required).
If not authenticated, instruct the user to run `gh auth login`.

Resolve the PR for the current branch: `gh pr view --json number,url,title,baseRefName`.
If there is no PR, stop and suggest /gh-open-pr.

## Workflow

The model is **collect → adjust**: Phase 1 gathers every input in parallel (review findings, PR comments, baseline check results); Phase 2 applies all fixes from that complete picture. Both are local and run without asking. Phase 3 ends with ONE approval gate covering everything outward-facing (push + thread replies). Phases 4-5 then run autonomously until CI is green.

### Phase 1 — Collect (everything read-only, all in parallel)

Self-contained — do not invoke other skills. The review criteria live in `references/review-checklist.md` (path relative to this skill's directory).

Launch ALL of the following concurrently — review agents in a single message, scripts/checks as background Bash:

1. **Review agents** (Agent tool, read-only — agents report findings, they do NOT edit). Each agent gets the diff scope (`git diff <base>...HEAD`), the path to `references/review-checklist.md`, and ONE lens:
   - `logic-edges` — logic errors, edge cases, error handling
   - `async-state` — async/concurrency, state & lifecycle
   - `contracts-security` — contract breaks, security, type safety
   - `quality` — the entire Pass 2 (reuse, simplification, dead weight, efficiency, altitude, consistency)

   Each agent must verify every finding against the actual file (not just the diff) and return: `file:line | what | evidence | suggested fix | confidence`.
   For tiny diffs (≲2 files / ≲100 lines), skip the fan-out and apply the checklist directly in the main context.

2. **Comments fetch** (background): `python scripts/fetch_comments.py` — prints conversation comments, reviews, and review threads (with `id` and `isResolved`) as JSON.
3. **Local checks** (background): detect the project's check commands, in this order of authority: project CLAUDE.md / docs, CI workflow files (`.github/workflows/`), then `package.json` scripts / `justfile` / `Makefile` / `pyproject.toml`. Run the full gate — lint, format check, typecheck, tests — as concurrent background shells when the commands are independent. Run what CI runs, not a subset (a typecheck step skipped locally is the classic "fails only in CI" source). This is a baseline run: it surfaces pre-existing failures early, while the review agents work.

### Phase 2 — Adjust (triage, apply fixes, green local checks)

1. **Triage**: for each **unresolved** thread from the comments fetch, classify:
   - **fix** — the comment makes sense: implement the change.
   - **answer** — disagree or not applicable: draft a short reply explaining why (no code change).
   - **unclear** — genuinely ambiguous: needs the user's call.
2. **Apply in the main context only** (agents never edit — single writer, no conflicts): deduplicate review findings against each other and against the comment fixes, re-check each against the file yourself, then apply high-confidence review fixes + **fix**-thread changes + baseline-check fixes to the working tree. Keep uncertain findings for the Phase 3 summary. Quality edits change zero behavior and touch only code this branch already changed.
3. **Re-run the local gate** (failed/affected checks first, then the full gate once) until clean.
4. Build the numbered triage table: `# | file:line | comment summary | verdict (fix/answer/unclear) | planned action/reply`.

### Phase 3 — Approval gate, then commit, push & reply

1. Show the user: triage table + summary of all local changes (quality pass + checks fixes + comment fixes). **Wait for approval.**
2. After approval:
   - Commit in logical units and push.
   - For each **fix** thread: reply with what was done + the commit sha, then resolve —
     `python scripts/reply_resolve_thread.py --thread-id <id> --body "Fixed in <sha>: <one-liner>"`
   - For each **answer** thread: reply with the explanation but do NOT resolve (the reviewer closes it) —
     `python scripts/reply_resolve_thread.py --thread-id <id> --body "..." --no-resolve`

### Phase 4 — Watch CI until green

1. Monitor: `gh pr checks <pr> --watch --interval 30` (or poll `python scripts/inspect_pr_checks.py --repo "." --pr <number> --json`).
2. All green → final summary, done.
3. Non-GitHub-Actions checks (Buildkite, CircleCI, etc.): report the details URL only, do not attempt to debug.

### Phase 5 — On CI failure: diagnose before edits

**DO NOT edit any source file until you have:**

1. Fetched and read the actual failure logs (multiple failing checks → fetch all logs concurrently as background Bash calls in one message):
   - `python scripts/inspect_pr_checks.py --repo "." --pr <number>` (extracts run IDs and failure snippets), or
   - `gh run view <run_id> --log-failed`; if "in progress", `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs"`
2. Identified the root cause with a specific log snippet as evidence.

Then fix, commit, push, and go back to Phase 4. Guessing the root cause wastes a full CI cycle (5-20 min); read the logs first.

**Loop limit:** after 3 failed fix cycles, stop and report to the user with the diagnosis of each attempt.

## Anti-Patterns (DO NOT)

- **DO NOT** edit files based on the check name alone without reading logs
- **DO NOT** assume the error from a previous run still applies — always fetch fresh logs
- **DO NOT** retry the same fix if it failed — re-diagnose with new logs
- **DO NOT** resolve a thread without replying to it first
- **DO NOT** resolve threads you answered with disagreement — leave those for the reviewer
- **DO NOT** push or reply to threads before the Phase 3 approval
- **DO NOT** make unrelated "while I'm at it" changes beyond what the review/comments call for

## Bundled Resources

### references/review-checklist.md

Two-pass diff review checklist used in Phase 1: correctness (bug-finding) criteria and quality (simplification) criteria.

### scripts/fetch_comments.py

Fetch all PR conversation comments, reviews, and review threads (with thread IDs and resolved state) for the current branch's PR, via `gh api graphql`. Prints JSON to stdout.

### scripts/reply_resolve_thread.py

Reply to a review thread and/or resolve it. `--thread-id` from fetch_comments.py output; `--body` for the reply; `--no-resolve` to reply without resolving.

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

- `python scripts/inspect_pr_checks.py --repo "." --pr "123"`
- `python scripts/inspect_pr_checks.py --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python scripts/inspect_pr_checks.py --repo "." --max-lines 200 --context 40`
