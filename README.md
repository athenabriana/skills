<div align="center">

# skills

[![github](https://img.shields.io/badge/github-athenabriana%2Fskills-111111?style=flat-square&logo=github)](https://github.com/athenabriana/skills)
[![spec](https://img.shields.io/badge/spec-agentskills.io-111111?style=flat-square)](https://agentskills.io)

_agent skills for claude code, cursor, codex, and any agent the [skills CLI](https://github.com/vercel-labs/skills) speaks to._

</div>

install all of them:

```bash
npx skills add athenabriana/skills
```

develop locally:

```bash
git clone git@github.com:athenabriana/skills.git
cd skills
bun install
bun validate
```

## what's inside

| skill                 | group | description                                                           |
| --------------------- | ----- | --------------------------------------------------------------------- |
| `shape`               | build | align on the idea before building — grill-me, lightweight brief, slices |
| `gh-open-pr`          | build | create a PR from the current branch                                   |
| `gh-address-comments` | build | address review comments on github PRs                                 |
| `gh-fix-pr`           | build | finalize and green a PR: review, simplify, checks, comments, CI watch |
| `branch-context`      | build | summarize all changes on the branch vs main                          |
| `improve-code`        | build | improve a diff's quality with a hard regression guard (no bugs)      |
| `gh-maintenance`      | loops | triage PRs + dependabot/outdated, report what's mergeable (never merges) |
| `gh-watch-pr`         | loops | supervised in-session loop that tends the current PR via gh-fix-pr   |
| `night-shift`         | loops | run one pre-shaped task overnight, ending at a draft PR (never merges) |
| `research-digest`     | loops | scheduled, read-only research/monitoring digest to slack or a branch |
| `gh-guardrails`       | loops | safety substrate for loops: no-merge hook, worktree isolation, self-test |
| `research-topic`      | utils | deep research using parallel agents                                  |
| `research-code`       | utils | find, clone, and explore relevant repos                             |
| `readme`              | utils | generate a minimal centered-header README from repo facts          |
| `take`                | utils | honest, decisive recommendation — commit, name the unseen tension, no sycophancy |

skills are grouped by **use**:

- **build** — write &amp; ship code, you-driven (shape → open-pr → fix-pr, plus improve-code / branch-context).
- **loops** — run across time, scheduled or event-driven, all sitting on `gh-guardrails`; set up as Cloud Routines (see each skill's `references/`).
- **utils** — standalone helpers (research, readme, take).

each skill folder is self-contained, `SKILL.md` plus optional `scripts/` and `references/` ship with the install.

<sub>`improve-code` is adapted from Claude Code's `/simplify` (Anthropic, Apache-2.0). individual components retain their original licenses.</sub>
