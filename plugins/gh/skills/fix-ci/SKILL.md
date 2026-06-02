---
name: gh-fix-ci
description: Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions. Uses `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treats external providers (for example Buildkite) as out of scope and reports only the details URL. Do NOT use for addressing PR review comments (use /gh-address-comments) or general CI outside GitHub Actions.
license: MIT
metadata:
  author: Athena Freitas - github.com/athenacfr
  version: 1.0.0
---

# Fix CI

Debug and fix failing GitHub Actions checks with evidence-based diagnosis.

## Critical Rule: Diagnosis Before Edits

**DO NOT edit any source files until you have:**

1. Fetched and read the actual failure logs
2. Identified the root cause with a specific log snippet as evidence
3. Presented the diagnosis to the user and received confirmation

Guessing the root cause and pushing a fix is the #1 failure pattern in CI debugging. Every fix attempt that fails wastes a full CI cycle (5-20 minutes). Get it right the first time by reading the logs.

## Prerequisites

Ensure `gh` is authenticated: `gh auth status` (repo + workflow scopes required).
If not authenticated, instruct the user to run `gh auth login`.

## Workflow

### Phase 1: Gather Evidence (MANDATORY)

1. **Resolve the PR**
   - Current branch: `gh pr view --json number,url`
   - Or use the PR number/URL the user provides

2. **Fetch failing checks**
   - Preferred: run the bundled script (path relative to this skill's directory)
     ```
     python scripts/inspect_pr_checks.py --repo "." --pr "<number-or-url>"
     ```
     Add `--json` for machine-friendly output.
   - Fallback:
     ```
     gh pr checks <pr> --json name,state,bucket,link,startedAt,completedAt,workflow
     ```

3. **Fetch failure logs** (for each failing GitHub Actions check)
   - Extract run ID from `detailsUrl`
   - Get run metadata: `gh run view <run_id> --json name,workflowName,conclusion,status,url,event,headBranch,headSha`
   - Get full logs: `gh run view <run_id> --log-failed`
   - If logs say "in progress", fetch job logs: `gh api "/repos/<owner>/<repo>/actions/jobs/<job_id>/logs"`

4. **Scope external checks**
   - Non-GitHub Actions checks (Buildkite, CircleCI, etc.): report the URL only, do not attempt to debug

### Phase 2: Diagnose (MANDATORY before any edits)

Present the diagnosis to the user in this format:

```
## CI Failure Diagnosis

### Failing Check: [check name]
- **Run URL**: [link]
- **Root Cause**: [specific explanation]
- **Evidence**:
```

[exact log snippet showing the failure]

```
- **Proposed Fix**: [what to change and why]
```

If there are multiple failing checks, diagnose each one separately.

**Wait for user confirmation before proceeding to Phase 3.**

### Phase 3: Fix (only after diagnosis is confirmed)

1. Implement the confirmed fix
2. Summarize what was changed and why
3. Ask about committing and pushing

### Phase 4: Verify

After the fix is pushed:

- `gh pr checks <pr>` to monitor the new run
- If the fix fails, go back to Phase 1 — fetch the NEW logs, don't guess again

## Anti-Patterns (DO NOT)

- **DO NOT** edit files based on the check name alone without reading logs
- **DO NOT** assume the error from a previous run still applies — always fetch fresh logs
- **DO NOT** retry the same fix if it failed — re-diagnose with new logs
- **DO NOT** make unrelated "while I'm at it" changes alongside the CI fix
- **DO NOT** loop more than 2 fix attempts without reporting to the user

## Bundled Resources

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage:

- `python scripts/inspect_pr_checks.py --repo "." --pr "123"`
- `python scripts/inspect_pr_checks.py --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python scripts/inspect_pr_checks.py --repo "." --max-lines 200 --context 40`
