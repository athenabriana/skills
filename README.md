# Athena Skills Marketplace

Claude Code plugins, also installable as standalone agent skills.

## Installation

### As Claude Code plugins (full experience: skills + hooks)

```bash
claude plugin marketplace add athenabriana/skills
claude plugin install gh@athena-skills research@athena-skills spec-driven@athena-skills skill-learner@athena-skills
```

### As standalone skills ([vercel-labs/skills](https://github.com/vercel-labs/skills) CLI)

```bash
npx skills add athenabriana/skills
```

Works with Claude Code, Cursor, Codex, and any agent the CLI supports. Note: `skill-learner` relies on plugin hooks, so its `review` skill is only useful with the plugin install.

## What's Inside

### Skills (user-invokable via `/skill-name`)

| Skill                 | Plugin        | Description                                  |
| --------------------- | ------------- | -------------------------------------------- |
| `gh-open-pr`          | gh            | Create a PR from the current branch          |
| `gh-address-comments` | gh            | Address review comments on GitHub PRs        |
| `gh-fix-ci`           | gh            | Evidence-based CI failure diagnosis and fix  |
| `branch-context`      | gh            | Summarize all changes on the branch vs main  |
| `research-topic`      | research      | Deep research using parallel agents          |
| `research-code`       | research      | Find, clone, and explore relevant repos      |
| `review`              | skill-learner | Review and manage auto-extracted skills      |
| `spec-create`         | spec-driven   | Define requirements and resolve gray areas   |
| `spec-design`         | spec-driven   | Architecture and component design            |
| `spec-run`            | spec-driven   | Break into tasks and implement               |

### Bundled scripts

Each skill is self-contained — its helper scripts live in the skill folder (`skills/<name>/scripts/`), so they ship with any install method.

| Script                      | Skill                 | Purpose                                                       |
| --------------------------- | --------------------- | ------------------------------------------------------------- |
| `gather_pr_context.py`      | `gh-open-pr`          | Collects branch, commits, diff, PR template in one call       |
| `fetch_comments.py`         | `gh-address-comments` | Fetches all PR comments and review threads via GraphQL        |
| `inspect_pr_checks.py`      | `gh-fix-ci`           | Fetches failing CI checks and extracts log snippets           |
| `gather_branch_context.py`  | `branch-context`      | Collects branch diff and commit context vs main               |
| `search_repos.py`           | `research-code`       | Searches GitHub by keyword + topic, dedupes, filters by stars |
| `list-pending-skills.py`    | `review`              | Lists auto-extracted skills awaiting review                   |
| `manage-skill.py`           | `review`              | Approve/reject/edit pending skills                            |

## Structure

```
plugins/
├── gh/
│   └── skills/open-pr/, address-comments/, fix-ci/, branch-context/
├── research/
│   └── skills/topic/, code/
├── skill-learner/
│   ├── hooks/                  # SessionStart + Stop hooks (plugin-only)
│   ├── scripts/                # hook scripts
│   └── skills/review/
└── spec-driven/
    └── skills/create/, design/, run/
```

## License

Individual components retain their original licenses.
