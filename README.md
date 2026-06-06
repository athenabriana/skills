<div align="center">

# skills

[![GitHub](https://img.shields.io/badge/github-athenabriana%2Fskills-111111?style=flat-square&logo=github)](https://github.com/athenabriana/skills)
[![Spec](https://img.shields.io/badge/spec-agentskills.io-111111?style=flat-square)](https://agentskills.io)

_Agent skills for Claude Code, Cursor, Codex, and any agent the [skills CLI](https://github.com/vercel-labs/skills) speaks to._

</div>

Install all of them:

```bash
npx skills add athenabriana/skills
```

Develop locally:

```bash
git clone git@github.com:athenabriana/skills.git
cd skills
bun install
bun validate
```

## What's inside

| Skill                 | Group       | Description                                                           |
| --------------------- | ----------- | --------------------------------------------------------------------- |
| `gh-open-pr`          | gh          | Create a PR from the current branch                                   |
| `gh-address-comments` | gh          | Address review comments on GitHub PRs                                 |
| `gh-fix-pr`           | gh          | Finalize and green a PR: review, simplify, checks, comments, CI watch |
| `branch-context`      | gh          | Summarize all changes on the branch vs main                           |
| `research-topic`      | research    | Deep research using parallel agents                                   |
| `research-code`       | research    | Find, clone, and explore relevant repos                               |
| `tlc-spec-driven`     | spec-driven | Spec-driven development: Specify, Design, Tasks, Execute              |
| `readme`              | docs        | Generate a minimal centered-header README from repo facts             |

Each skill folder is self-contained — `SKILL.md` plus optional `scripts/` and `references/` ship with the install.

<sub>`tlc-spec-driven` is based on [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) (CC-BY-4.0). Individual components retain their original licenses.</sub>
