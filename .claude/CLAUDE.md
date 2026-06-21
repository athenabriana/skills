# Skills

A **Claude Code plugin** (`ath`) published through a one-plugin marketplace. Install via `claude plugin marketplace add athenabriana/skills` then `claude plugin install ath@athenabriana`. Skills are invoked as `/ath:<skill>` (e.g. `/ath:build-ship-pr`). The plugin ships a `PreToolUse` no-merge guard hook and a `SessionStart` operating-context hook, both auto-active when the plugin is enabled.

## Structure

```
.claude-plugin/marketplace.json        # lists the single `ath` plugin
plugins/ath/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── hooks.json                      # PreToolUse no-merge guard + SessionStart context
│   ├── inject_operating_context.py     # SessionStart hook script
│   └── operating-context.md            # the injected operating frame (edit to tune)
└── skills/                             # all skills flat; names carry a use-group prefix
    ├── build-shape, build-implement, build-ship-pr, build-address-comments, build-branch-context, build-improve-code
    ├── loop-maintenance, loop-watch-pr, loop-night-shift, loop-digest, loop-guardrails
    └── util-topic, util-code, util-readme, util-take
```

### Naming Conventions

- Skills live in `plugins/ath/skills/<name>/SKILL.md`. The frontmatter `name` carries a **use-group prefix** — `build-` (write & ship), `loop-` (run across time), `util-` (helpers) — e.g. `build-ship-pr`, `util-take`. It's invoked as `/ath:<name>` (`/ath:build-ship-pr`), so the group is visible at the call site. The prefix is part of the name; keep it consistent with the skill's group and match the dir name to it.
- Each skill is self-contained: `scripts/` and `references/*.md` relative to the skill dir.
- The plugin ships hooks in `plugins/ath/hooks/hooks.json` (auto-activate when the plugin is enabled). Use them to enforce irreversible hazards (the no-merge guard) and to inject session-start context. Hook commands reference files via `${CLAUDE_PLUGIN_ROOT}/...` (e.g. `${CLAUDE_PLUGIN_ROOT}/skills/loop-guardrails/scripts/guard_irreversible.py`).

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
- Keep guidance positive and lean by default — enforce irreversible hazards with hooks (see `/ath:loop-guardrails`), not prose. Don't write catalogs of anti-patterns / "DO NOT" lists; they're context noise and a weaker signal. A single sharp caution is allowed where negation is genuinely the clearest signal (e.g. a skill warning about its own failure mode) — the ban is on lists and reflexive negation, not on ever saying "don't".
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
- Scope is the skill name (`build-shape`, `loop-maintenance`, …), the use-group (`build`/`loop`/`util`) when a change spans one, `hooks` for the hook layer, or `repo` for repo-wide changes
