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

| skill                 | group    | mode   | description                                                           |
| --------------------- | -------- | ------ | --------------------------------------------------------------------- |
| `gh-open-pr`          | gh       | manual | create a PR from the current branch                                   |
| `gh-address-comments` | gh       | manual | address review comments on github PRs                                 |
| `gh-fix-pr`           | gh       | manual | finalize and green a PR: review, simplify, checks, comments, CI watch |
| `gh-maintenance`      | gh       | loop   | triage PRs + dependabot/outdated, report what's mergeable (never merges) |
| `gh-watch-pr`         | gh       | loop   | supervised in-session loop that tends the current PR via gh-fix-pr    |
| `gh-guardrails`       | gh       | infra  | safety substrate for loops: no-merge hook, worktree isolation, self-test |
| `branch-context`      | gh       | manual | summarize all changes on the branch vs main                          |
| `research-topic`      | research | manual | deep research using parallel agents                                  |
| `research-code`       | research | manual | find, clone, and explore relevant repos                             |
| `research-digest`     | research | loop   | scheduled, read-only research/monitoring digest to slack or a branch |
| `shape`               | build    | manual | align on the idea before building — grill-me, lightweight brief, slices |
| `night-shift`         | build    | loop   | run one pre-shaped task overnight, ending at a draft PR (never merges) |
| `improve-code`        | quality  | manual | improve a diff's quality with a hard regression guard (no bugs)      |
| `readme`              | docs     | manual | generate a minimal centered-header README from repo facts           |

skills are grouped by **flow** (the manual + loop skills of a flow stay together) and tagged by **mode**:

- **manual** — you run it on demand.
- **loop** — runs across time (scheduled or event-driven). the **autonomy suite** is `gh-maintenance`, `gh-watch-pr`, `night-shift`, `research-digest`, all sitting on `gh-guardrails` (mode `infra`). set up as Cloud Routines — see each skill's `references/`.

each skill folder is self-contained, `SKILL.md` plus optional `scripts/` and `references/` ship with the install.

<sub>`improve-code` is adapted from Claude Code's `/simplify` (Anthropic, Apache-2.0). individual components retain their original licenses.</sub>
