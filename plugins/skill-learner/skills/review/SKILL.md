---
name: review
description: Review and manage pending auto-extracted skills. Use when user says "review skills", "check pending skills", "approve skills", "manage learned skills", or when the SessionStart hook reports pending skills.
license: MIT
metadata:
  author: Athena Freitas - github.com/athenacfr
  version: 1.0.0
---

# Review Pending Skills

Interactive review of auto-extracted skills waiting in `~/.claude/skills/review/`.

## Workflow

### 1. List Pending Skills

Run the listing script (path relative to this skill's directory):

```
python3 scripts/list-pending-skills.py
```

Returns JSON with all pending skills (sorted by confidence) and folder counts.

If no pending skills, tell the user and stop.

### 2. Present Summary

Show a table of pending skills:

```
| # | Skill                  | Confidence | Occurrences | Scope   |
|---|------------------------|------------|-------------|---------|
| 1 | debug-port-conflicts   | 0.85       | 4           | global  |
| 2 | fix-prisma-migrations  | 0.70       | 3           | global  |
| 3 | react-form-patterns    | 0.60       | 2           | global  |
```

Also show counts: "3 pending, N active, N rejected"

### 3. Review Loop

Ask the user how they want to proceed. Support these modes:

**Batch mode** (user says "approve all", "approve all above 0.7", etc.):

- Filter by the condition
- Run the manage script for each matching skill

**One-by-one mode** (default):
For each skill, starting with highest confidence:

1. Show the skill name, confidence, scope, and occurrence count
2. Show the "When to Use" section
3. Show the "Procedure" section (the key steps)
4. If gotchas exist, show them
5. Ask: **approve, reject, edit, or skip?**

### 4. Execute Actions

For each decision, run:

```
python3 scripts/manage-skill.py <action> <skill-name>
```

Where `<action>` is `approve`, `reject`, or `skip`.

**If the user chooses "edit":**

1. Read the full skill file from `~/.claude/skills/review/<skill-name>.md`
2. Ask what they want to change
3. Apply edits with the Edit tool
4. Then ask again: approve or reject the edited version

### 5. Summary

After all skills are reviewed, show what happened:

```
Review complete:
  Approved: debug-port-conflicts, fix-prisma-migrations
  Rejected: (none)
  Skipped: react-form-patterns (still in review/)
```
