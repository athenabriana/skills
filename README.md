<div align="center">

# skills

[![github](https://img.shields.io/badge/github-athenabriana%2Fskills-111111?style=flat-square&logo=github)](https://github.com/athenabriana/skills)

_a claude code plugin — agent skills grouped by use, with an operating-context hook shipped alongside them._

</div>

add the marketplace, then install the one plugin:

```bash
claude plugin marketplace add athenabriana/skills
claude plugin install ath@athenabriana
```

it ships a `SessionStart` operating-context hook, auto-active on install. skills are invoked as `/ath:<skill>` — e.g. `/ath:shape`, `/ath:night-shift`, `/ath:answer-yourself`.

## what's inside

one plugin, `ath`; the skills are organized by use.

### shape & ship — write & ship code, you-driven

| skill                        | description                                                                                                                                                              |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/ath:shape`                 | align on the idea before building — develop, loop on gray areas via questions, validate                                                                                  |
| `/ath:implement`             | implement a validated shape brief — build the slices, run the gate, stop ready to ship                                                                                   |
| `/ath:ship`                  | land the branch your way — review + green the checks, then push to a branch, prep a push to main, or open a PR & auto-tend it (handle comments, green CI, keep watching) |
| `/ath:address-comments`      | address review comments on github PRs                                                                                                                                    |
| `/ath:gather-branch-context` | summarize all changes on the branch vs main                                                                                                                              |
| `/ath:improve-code`          | improve a diff's quality with a hard regression guard (no bugs)                                                                                                          |

### loops — run across time (scheduled / event-driven)

for the unattended (Cloud Routine) path, never-merge is enforced by **capability scoping** — the routine runs with a token that has no merge/branch-push permission and no merge-capable connector — backed by GitHub branch protection. Server-side controls, not a local hook.

| skill                  | description                                                              |
| ---------------------- | ------------------------------------------------------------------------ |
| `/ath:maintain-repo`   | triage PRs + dependabot/outdated, report what's mergeable (never merges) |
| `/ath:night-shift`     | run one pre-shaped task overnight, ending at a draft PR (never merges)   |
| `/ath:digest-research` | scheduled, read-only research/monitoring digest to slack or a branch     |

### helpers — standalone

| skill                  | description                                                                      |
| ---------------------- | -------------------------------------------------------------------------------- |
| `/ath:research-topic`  | deep research using parallel agents                                              |
| `/ath:research-code`   | find, clone, and explore relevant repos                                          |
| `/ath:write-readme`    | generate a minimal centered-header README from repo facts                        |
| `/ath:answer-yourself` | honest, decisive recommendation — commit, name the unseen tension, no sycophancy |

develop locally:

```bash
git clone git@github.com:athenabriana/skills.git
claude --plugin-dir ./skills/plugins/ath    # load the plugin from disk to test
```

<sub>`/ath:improve-code` is adapted from Claude Code's `/simplify` (Anthropic, Apache-2.0). individual components retain their original licenses.</sub>
