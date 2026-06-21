# Skills

A **Claude Code plugin marketplace**: three plugins (`build`, `loops`, `utils`) grouped by use. Install via `claude plugin marketplace add athenabriana/skills` then `claude plugin install <plugin>@athenabriana`. Skills are invoked as `/<plugin>:<skill>` (e.g. `/build:fix-pr`). The `loops` plugin ships a `PreToolUse` guard hook that auto-activates on install.

## Structure

```
.claude-plugin/marketplace.json    # lists the build / loops / utils plugins
plugins/
├── build/                         # write & ship code, you-driven
│   ├── .claude-plugin/plugin.json
│   └── skills/  → shape, open-pr, address-comments, fix-pr, branch-context, improve-code
├── loops/                         # run across time (scheduled / event-driven)
│   ├── .claude-plugin/plugin.json
│   ├── hooks/hooks.json           # the no-merge PreToolUse guard — auto-activates
│   └── skills/  → maintenance, watch-pr, night-shift, digest, guardrails
└── utils/                         # standalone helpers
    ├── .claude-plugin/plugin.json
    └── skills/  → topic, code, readme, take
```

### Naming Conventions

- Skills live in `plugins/<plugin>/skills/<name>/SKILL.md`. The frontmatter `name` is **bare** (e.g. `fix-pr`, `take`) — the plugin namespace supplies the prefix, so the skill is invoked as `/<plugin>:<name>` (`/build:fix-pr`). Do not put the group in the name.
- Each skill is self-contained: `scripts/` and `references/*.md` relative to the skill dir.
- A plugin ships hooks in `plugins/<plugin>/hooks/hooks.json` (auto-activate when the plugin is enabled). Use them to enforce irreversible hazards — see the `loops` no-merge guard. Hook commands reference scripts via `${CLAUDE_PLUGIN_ROOT}/skills/<name>/scripts/...`.

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
- No anti-pattern / "DO NOT" lists — enforce irreversible hazards with hooks (see `/loops:guardrails`); keep guidance positive and lean (negative lists are context noise and a weaker signal for the model)
- Use `references/` for static context the LLM needs (coding principles, validation checklists)
- Trigger descriptions should be specific — list exact phrases the user might say
- Skill workflows reference their own scripts relatively (e.g. `scripts/foo.py`). Only **hooks** use `${CLAUDE_PLUGIN_ROOT}` (the plugin's absolute install path) — skill bodies should not.

## Scripts

- Python scripts use `gh api graphql` for GitHub data (not the REST API directly)
- Scripts are invoked via `Bash` tool from within skill workflows
- Scripts write to stdout (JSON or plain text) for the LLM to consume
- New scripts should use Python, stdlib only (no third-party imports)

## Commits

- No AI attribution in commits, PRs, or code comments
- Conventional commit style: `<type>(<scope>): <description>`
- Scope should be the skill group name (`build`, `loops`, `utils`) or `repo` for repo-wide changes
