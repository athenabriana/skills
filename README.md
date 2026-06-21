<div align="center">

# skills

[![github](https://img.shields.io/badge/github-athenabriana%2Fskills-111111?style=flat-square&logo=github)](https://github.com/athenabriana/skills)

_a claude code plugin — agent skills grouped by use, with the guardrail hook and an operating-context hook shipped alongside them._

</div>

add the marketplace, then install the one plugin:

```bash
claude plugin marketplace add athenabriana/skills
claude plugin install ath@athenabriana
```

it ships a `PreToolUse` no-merge guard hook and a `SessionStart` operating-context hook, both auto-active on install. skills are invoked as `/ath:<skill>` — e.g. `/ath:shape`, `/ath:night-shift`, `/ath:take`.

## what's inside

one plugin, `ath`; the skills are organized by use.

### shape & ship — write & ship code, you-driven

| skill | description |
| ------------------------- | --------------------------------------------------------------------- |
| `/ath:shape`            | align on the idea before building — develop, loop on gray areas via questions, validate |
| `/ath:open-pr`          | create a PR from the current branch                                   |
| `/ath:address-comments` | address review comments on github PRs                                 |
| `/ath:fix-pr`           | finalize and green a PR: review, simplify, checks, comments, CI watch |
| `/ath:branch-context`   | summarize all changes on the branch vs main                           |
| `/ath:improve-code`     | improve a diff's quality with a hard regression guard (no bugs)       |

### loops — run across time (scheduled / event-driven)

these run on the no-merge guard hook (blocks merge / approve / force-push / branch-delete).

| skill | description |
| --------------------- | --------------------------------------------------------------------- |
| `/ath:maintenance`  | triage PRs + dependabot/outdated, report what's mergeable (never merges) |
| `/ath:watch-pr`     | supervised in-session loop that tends the current PR via `/ath:fix-pr` |
| `/ath:night-shift`  | run one pre-shaped task overnight, ending at a draft PR (never merges) |
| `/ath:digest`       | scheduled, read-only research/monitoring digest to slack or a branch  |
| `/ath:guardrails`   | the safety substrate: tier-1/2 boundary, worktree isolation, the guard hook + self-test |

### helpers — standalone

| skill | description |
| --------------- | --------------------------------------------------------------------- |
| `/ath:topic`  | deep research using parallel agents                                   |
| `/ath:code`   | find, clone, and explore relevant repos                               |
| `/ath:readme` | generate a minimal centered-header README from repo facts             |
| `/ath:take`   | honest, decisive recommendation — commit, name the unseen tension, no sycophancy |

develop locally:

```bash
git clone git@github.com:athenabriana/skills.git
claude --plugin-dir ./skills/plugins/ath    # load the plugin from disk to test
```

<sub>`/ath:improve-code` is adapted from Claude Code's `/simplify` (Anthropic, Apache-2.0). individual components retain their original licenses.</sub>
