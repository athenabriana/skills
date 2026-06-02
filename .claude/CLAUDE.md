# Skills Marketplace

A Claude Code plugin marketplace containing four plugin groups: `gh`, `research`, `skill-learner`, and `spec-driven`. Also installable standalone via the [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI (`npx skills add athenabriana/skills`), which discovers skills through `marketplace.json`.

## Structure

```
plugins/
├── gh/                          # GitHub PR workflows
│   ├── .claude-plugin/plugin.json
│   └── skills/open-pr/, address-comments/, fix-ci/, branch-context/
├── research/                    # Topic & code research
│   ├── .claude-plugin/plugin.json
│   └── skills/topic/, code/
├── skill-learner/               # Background session learning
│   ├── .claude-plugin/plugin.json
│   ├── hooks/hooks.json         # SessionStart + Stop hooks
│   ├── scripts/                 # hook-only scripts (on-stop, extract, parse, check)
│   ├── references/
│   └── skills/review/
└── spec-driven/                 # Spec-driven development
    ├── .claude-plugin/plugin.json
    └── skills/create/, design/, run/
```

Marketplace metadata: `.claude-plugin/marketplace.json` (root), per-plugin: `plugins/<name>/.claude-plugin/plugin.json`.

### Naming Conventions

- Skills live in `plugins/<group>/skills/<name>/SKILL.md`; the frontmatter `name` carries the group prefix (e.g. `gh-fix-ci`)
- Each skill is self-contained: its scripts live in `skills/<name>/scripts/`, reference docs in `skills/<name>/references/*.md`
- Plugin-level `scripts/` is reserved for hook scripts (only `skill-learner` has them) — hooks resolve via `${CLAUDE_PLUGIN_ROOT}`, which only exists in plugin context

## Skills

Each skill is a folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`, `license`, `metadata`) followed by Markdown instructions. The `description` field doubles as the trigger — it tells Claude Code when to invoke the skill.

Skills may include a `references/` subfolder with supplementary Markdown docs that get loaded as context. Skills use built-in Claude Code subagent types (`research:web-researcher`, `research:doc-analyst`, `research:repo-explorer`) — no custom agent definitions needed.

### Scripting Principle

Skills are folders — they can contain scripts alongside the SKILL.md. **Prefer Python scripts for deterministic operations** (parsing, formatting, data transformation, file manipulation, JSON processing) over having the LLM do it inline. Scripts run faster, cost zero tokens, and produce consistent results. Reserve LLM reasoning for judgment calls, synthesis, and creative decisions.

Examples of what should be a script:

- Parsing GraphQL/REST responses into structured data
- Generating file paths or boilerplate from templates
- Validating JSON schemas or config files
- Transforming markdown between formats

### Writing Guidelines

- Keep SKILL.md focused on the workflow and decision-making logic
- Use `references/` for static context the LLM needs (coding principles, validation checklists)
- Trigger descriptions should be specific — list exact phrases the user might say
- Reference skill scripts by path relative to the skill's directory (e.g. `scripts/foo.py`) — never `${CLAUDE_PLUGIN_ROOT}`, which breaks standalone installs (vercel CLI copies only the skill folder)

## Scripts

- Python scripts use `gh api graphql` for GitHub data (not the REST API directly)
- Scripts are invoked via `Bash` tool from within skill workflows
- Scripts write to stdout (JSON or plain text) for the LLM to consume
- New scripts should use Python, stdlib only (no third-party imports)

## Commits

- No AI attribution in commits, PRs, or code comments
- Conventional commit style: `<type>(<scope>): <description>`
- Scope should be the plugin group name: `gh`, `research`, `spec-driven`, or `marketplace`
