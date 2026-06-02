# Athena Skills

Agent skills following the [Agent Skills](https://agentskills.io) spec. Works with Claude Code, Cursor, Codex, and any agent supported by the [skills CLI](https://github.com/vercel-labs/skills).

## Installation

```bash
npx skills add athenabriana/skills
```

## What's Inside

### Skills (user-invokable via `/skill-name`)

| Skill                 | Group       | Description                                                                                                                              |
| --------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `gh-open-pr`          | gh          | Create a PR from the current branch                                                                                                      |
| `gh-address-comments` | gh          | Address review comments on GitHub PRs                                                                                                    |
| `gh-fix-ci`           | gh          | Evidence-based CI failure diagnosis and fix                                                                                              |
| `branch-context`      | gh          | Summarize all changes on the branch vs main                                                                                              |
| `research-topic`      | research    | Deep research using parallel agents                                                                                                      |
| `research-code`       | research    | Find, clone, and explore relevant repos                                                                                                  |
| `tlc-spec-driven`     | spec-driven | Spec-driven development: Specify, Design, Tasks, Execute ([tech-leads-club](https://github.com/tech-leads-club/agent-skills), CC-BY-4.0) |

### Bundled scripts

Each skill is self-contained — its helper scripts live in the skill folder (`scripts/`), so they ship with the install.

| Script                     | Skill                 | Purpose                                                       |
| -------------------------- | --------------------- | ------------------------------------------------------------- |
| `gather_pr_context.py`     | `gh-open-pr`          | Collects branch, commits, diff, PR template in one call       |
| `fetch_comments.py`        | `gh-address-comments` | Fetches all PR comments and review threads via GraphQL        |
| `inspect_pr_checks.py`     | `gh-fix-ci`           | Fetches failing CI checks and extracts log snippets           |
| `gather_branch_context.py` | `branch-context`      | Collects branch diff and commit context vs main               |
| `search_repos.py`          | `research-code`       | Searches GitHub by keyword + topic, dedupes, filters by stars |

## Structure

```
skills/
├── gh/            open-pr/, address-comments/, fix-ci/, branch-context/
├── research/      topic/, code/
└── spec-driven/   tlc-spec-driven/
```

Each skill folder holds a `SKILL.md` plus optional `scripts/` and `references/`.

## License

Individual components retain their original licenses.
