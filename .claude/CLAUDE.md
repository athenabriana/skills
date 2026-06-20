# Skills

A repo of agent skills following the [Agent Skills](https://agentskills.io) spec, installable via the [vercel-labs/skills](https://github.com/vercel-labs/skills) CLI: `npx skills add athenabriana/skills`. The CLI auto-discovers the catalog layout `skills/<group>/<name>/SKILL.md`.

## Structure

```
skills/
├── gh/                          # GitHub PR workflows + autonomy
│   └── open-pr/, address-comments/, fix-pr/, maintenance/, watch-pr/, guardrails/, branch-context/
├── research/                    # research + scheduled digest
│   └── topic/, code/, digest/
├── build/                       # shape the idea, build it overnight
│   └── shape/, night-shift/
└── quality/                     # code quality
    └── improve-code/            # adapted from Claude Code /simplify (Apache-2.0)
```

### Naming Conventions

- Skills live in `skills/<group>/<name>/SKILL.md`; the frontmatter `name` carries the group prefix (e.g. `gh-fix-pr`) since it becomes the install directory name
- Each skill is self-contained: scripts in `skills/<group>/<name>/scripts/`, reference docs in `skills/<group>/<name>/references/*.md`

## Skills

Each skill is a folder with a `SKILL.md` containing YAML frontmatter (`name`, `description`, `license`, `metadata`) followed by Markdown instructions. The `description` field doubles as the trigger — it tells the agent when to invoke the skill.

Skills may include a `references/` subfolder with supplementary Markdown docs that get loaded as context.

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
- Reference skill scripts by path relative to the skill's directory (e.g. `scripts/foo.py`) — never `${CLAUDE_PLUGIN_ROOT}`, which only exists in Claude Code plugin context and breaks standalone installs

## Scripts

- Python scripts use `gh api graphql` for GitHub data (not the REST API directly)
- Scripts are invoked via `Bash` tool from within skill workflows
- Scripts write to stdout (JSON or plain text) for the LLM to consume
- New scripts should use Python, stdlib only (no third-party imports)

## Commits

- No AI attribution in commits, PRs, or code comments
- Conventional commit style: `<type>(<scope>): <description>`
- Scope should be the skill group name (`gh`, `research`, `build`, `quality`, `docs`) or `repo` for repo-wide changes
