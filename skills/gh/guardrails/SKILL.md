---
name: gh-guardrails
description: The safety substrate for any unattended/across-time run. Installs and verifies the layer that MUST accompany increased autonomy — a deterministic PreToolUse hook that blocks tier-2 (irreversible) operations, git-worktree isolation for local autonomous runs, a two-tier reversible/irreversible boundary, and an active self-test that proves the guard is live before a run proceeds. Use when the user says "make this safe to run unattended", "install the autonomy guardrails", "set up the no-merge hook", or "what can run without me". Pair this with every loop/overnight/scheduled skill. Do NOT use to do the work itself (see /gh-watch-pr, /gh-maintenance, /research-digest, /shape).
license: MIT
metadata:
  author: Athena Briana - github.com/athenabriana
  version: 1.0.0
---

# Autonomy Guardrails

The rule for across-time autonomy: **as human supervision drops, push each safety guarantee DOWN the stack** — from "the model follows the skill" → "the harness enforces the hook" → "the capability was never granted." Prose in a skill is the weakest place for a safety-critical rule, because that is exactly the layer prompt-injection attacks. This skill is the bottom two layers.

## The three layers (install all three before any unattended write)

1. **Withheld capability (strongest).** The run simply cannot do the dangerous thing. For a Cloud Routine: a GitHub token/App installation without merge permission, "Allow unrestricted branch pushes" OFF, and no merge-capable connector attached. Nothing below matters if this is wrong — see `references/autonomy-boundary.md`.
2. **Deterministic hook (harness-enforced).** `scripts/guard_irreversible.py` as a `PreToolUse` hook denies tier-2 ops (merge, approve, force-push, protected-branch push, branch delete, untrusted deploy, recursive wipe) regardless of model cooperation. Commit `references/settings.example.json` into the **target repo's** `.claude/settings.json` — a local-only hook does NOT propagate to a cloud routine's fresh clone.
3. **Active self-test (fail-closed).** `scripts/selftest_guard.py` fires known-bad probes through the hook and asserts each is denied. Run it as the FIRST step of any unattended run; if it fails, ABORT — an unwired hook is the ultimate bypass. For cloud, do a one-off probe `Run now` to confirm routines honor the repo-committed hook (this is unverified by default — if the probe is not denied, rely solely on layer 1).

## Blast-radius isolation (local runs)

For local / Desktop-scheduled autonomous runs and parallel tasks, run inside a throwaway worktree: `python scripts/enter_worktree.py --label <skill>`. It fails closed — refuses on a protected branch or a dirty tree — so an autonomous run can never touch the live checkout or a protected branch. (A Cloud Routine already isolates via its disposable fresh clone + `claude/` branch and does NOT need this.)

## Picking a mechanism

`references/scheduling-decision.md` is the decision table for `/loop` vs Desktop task vs Cloud Routine vs Channels vs `/goal` vs the Monitor tool, with their real limits — so an AFK overnight job is never scheduled as a session `/loop` that silently dies.

## Anti-Patterns (DO NOT)

- **DO NOT** treat the hook as the primary control — it is a tripwire behind withheld capability. A determined model can route around any string matcher.
- **DO NOT** rely on Auto Mode classifiers as a substitute for human review on tier-2 actions — their adversarial robustness is contested (~17% vendor vs ~81% independent false-negative rate).
- **DO NOT** run an unattended write without passing `selftest_guard.py` first.
- **DO NOT** commit the hook only to your local `~/.claude` and assume a cloud routine honors it — it must be in the target repo.

## Bundled Resources

### scripts/guard_irreversible.py
PreToolUse hook denying tier-2 ops (Windows/PowerShell-aware). Reads optional extra deny patterns from `.claude/autonomy-boundary.json`; enforces built-in defaults fail-closed.

### scripts/enter_worktree.py
Creates/reuses an isolated worktree on a throwaway `auto/<label>` branch; fails closed on a protected branch or dirty tree. Emits JSON.

### scripts/selftest_guard.py
Fires deny/allow probes through the guard and exits non-zero on mismatch — the gate before any unattended run.

### references/autonomy-boundary.md
The tier-1 (reversible, may run unattended) vs tier-2 (irreversible, human-only) boundary, the capability-first principle, and the `.claude/autonomy-boundary.json` schema.

### references/scheduling-decision.md
Decision table for the scheduling/trigger mechanisms and their real limits.

### references/settings.example.json
The `.claude/settings.json` PreToolUse hook block to commit into the target repo.
