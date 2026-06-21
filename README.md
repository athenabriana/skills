<div align="center">

# skills

[![github](https://img.shields.io/badge/github-athenabriana%2Fskills-111111?style=flat-square&logo=github)](https://github.com/athenabriana/skills)

_a claude code plugin marketplace — agent skills grouped by use, with the guardrail hook shipped alongside the loops that need it._

</div>

add the marketplace, then install the plugin(s) you want:

```bash
claude plugin marketplace add athenabriana/skills
claude plugin install build@athenabriana
claude plugin install loops@athenabriana    # ships the no-merge guardrail hook
claude plugin install utils@athenabriana
```

skills are invoked as `/<plugin>:<skill>` — e.g. `/build:fix-pr`, `/loops:night-shift`, `/utils:take`.

## what's inside

### `build` — write & ship code, you-driven

| skill | description |
| ------------------------- | --------------------------------------------------------------------- |
| `/build:shape`            | align on the idea before building — draft-first brief, react & revise, slices |
| `/build:open-pr`          | create a PR from the current branch                                   |
| `/build:address-comments` | address review comments on github PRs                                 |
| `/build:fix-pr`           | finalize and green a PR: review, simplify, checks, comments, CI watch |
| `/build:branch-context`   | summarize all changes on the branch vs main                           |
| `/build:improve-code`     | improve a diff's quality with a hard regression guard (no bugs)       |

### `loops` — run across time (scheduled / event-driven)

ships a `PreToolUse` guard hook (blocks merge / approve / force-push / branch-delete) that **auto-activates** when the plugin is enabled.

| skill | description |
| --------------------- | --------------------------------------------------------------------- |
| `/loops:maintenance`  | triage PRs + dependabot/outdated, report what's mergeable (never merges) |
| `/loops:watch-pr`     | supervised in-session loop that tends the current PR via `/build:fix-pr` |
| `/loops:night-shift`  | run one pre-shaped task overnight, ending at a draft PR (never merges) |
| `/loops:digest`       | scheduled, read-only research/monitoring digest to slack or a branch  |
| `/loops:guardrails`   | the safety substrate: tier-1/2 boundary, worktree isolation, the guard hook + self-test |

### `utils` — standalone helpers

| skill | description |
| --------------- | --------------------------------------------------------------------- |
| `/utils:topic`  | deep research using parallel agents                                   |
| `/utils:code`   | find, clone, and explore relevant repos                               |
| `/utils:readme` | generate a minimal centered-header README from repo facts             |
| `/utils:take`   | honest, decisive recommendation — commit, name the unseen tension, no sycophancy |

develop locally:

```bash
git clone git@github.com:athenabriana/skills.git
claude --plugin-dir ./skills/plugins/loops    # load a plugin from disk to test
```

<sub>`/build:improve-code` is adapted from Claude Code's `/simplify` (Anthropic, Apache-2.0). individual components retain their original licenses.</sub>
