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

| skill                 | group       | description                                                           |
| --------------------- | ----------- | --------------------------------------------------------------------- |
| `gh-open-pr`          | gh          | create a PR from the current branch                                   |
| `gh-address-comments` | gh          | address review comments on github PRs                                 |
| `gh-fix-pr`           | gh          | finalize and green a PR: review, simplify, checks, comments, CI watch |
| `gh-maintenance`      | gh          | triage PRs + dependabot/outdated deps, report what's mergeable (never merges) |
| `gh-watch-pr`         | gh          | supervised in-session loop that tends the current PR via gh-fix-pr     |
| `gh-guardrails`       | gh          | safety substrate for unattended runs: no-merge hook, worktree isolation, self-test |
| `branch-context`      | gh          | summarize all changes on the branch vs main                           |
| `research-topic`      | research    | deep research using parallel agents                                   |
| `research-code`       | research    | find, clone, and explore relevant repos                               |
| `research-digest`     | research    | scheduled, read-only research/monitoring digest to slack or a branch  |
| `tlc-spec-driven`     | spec-driven | spec-driven development: specify, design, tasks, execute              |
| `overnight-spec`      | spec-driven | run one pre-written spec task overnight, ending at a draft PR (never merges) |
| `quality-simplify`    | quality     | review a diff for quality and apply behavior-preserving cleanups (no bug-hunting) |
| `readme`              | docs        | generate a minimal centered-header README from repo facts             |

each skill folder is self-contained, `SKILL.md` plus optional `scripts/` and `references/` ship with the install.

<sub>`tlc-spec-driven` is based on [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) (CC-BY-4.0). individual components retain their original licenses.</sub>

<sub>`quality-simplify` is adapted from Claude Code's `/simplify` (Anthropic, Apache-2.0). individual components retain their original licenses.</sub>
