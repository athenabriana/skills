# The autonomy boundary — tier-1 vs tier-2

The single decision that makes unattended work safe: split every action by
**reversibility**, let only the reversible class run without a human, and make
the irreversible class structurally impossible (not just "discouraged").

## Tier-1 — reversible (may run unattended)

- read / scan / fetch (GitHub API GETs, CI conclusions, logs)
- post or edit a comment (a sticky digest comment)
- commit and push to a **throwaway** branch (`auto/*`) or a `claude/`-prefixed branch
- open a **draft** PR
- reply to a review thread (without resolving someone else's disagreement)

These are recoverable: a bad branch is deleted, a draft PR is closed, a comment
is edited. The blast radius is a branch, never `main`.

## Tier-2 — irreversible (human-only, even with Auto Mode)

- `gh pr merge` / the `mergePullRequest` GraphQL mutation
- approving a PR
- `git push --force` / `--force-with-lease`
- pushing to a protected/default branch
- deleting a branch
- `lexflow deploy` (without `--dry-run`), or any deploy
- mutating a secret or a connection
- **executing untrusted dependency code** (`bun install`/`bun test` on an
  unreviewed update) — this is irreversible in the sense that arbitrary code has
  already run; do it only in a sandbox you control

The human-review/land step lives here. Research is unambiguous: review capacity
is the binding constraint, and these vendor mechanisms are "not a drop-in
replacement for careful human review."

## Enforce in this order (capability first)

1. **Withhold the capability.** The routine's token/App lacks merge permission;
   no merge-capable connector is attached; "unrestricted branch pushes" is OFF.
   This is the only layer that holds regardless of model behavior or hook
   support.
2. **Block with the hook.** `guard_irreversible.py` denies the tier-2 command
   strings as defense-in-depth.
3. **State it in the skill.** Prose is the last layer and the weakest — never the
   only one.

## `.claude/autonomy-boundary.json` (optional extra deny patterns)

`guard_irreversible.py` always enforces the built-in tier-2 defaults and, if this
file exists, ALSO enforces extra patterns from it. Use it to add repo-specific
irreversible commands (e.g. a custom deploy script).

```json
{
  "deny_patterns": [
    { "label": "publish a package", "pattern": "\\bnpm\\s+publish\\b|\\bbun\\s+publish\\b" },
    { "label": "run the deploy script", "pattern": "\\b(\\./)?scripts/deploy\\.sh\\b" }
  ]
}
```

Patterns are case-insensitive Python regexes matched against the normalized
command (leading `VAR=...` assignments stripped, whitespace collapsed). A present
-but-unparseable file falls back to the built-in defaults (fail-closed for the
dangerous class) and logs to stderr.
