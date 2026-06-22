# Repo knowledge base (.ath/knowledge/, OKF)

## What & why

A repo-local, git-committed knowledge base under `.ath/knowledge/` in **OKF**
(Open Knowledge Format — a directory of markdown files with YAML frontmatter,
one required field `type`). It holds curated, citable domain knowledge shared
with the team — distinct from Claude Code's per-user, cross-session memory
(`~/.claude/.../memory/`), which stays personal.

First and best consumer: **legal-lens**. Today the lens is grounded only by its
own reasoning + live web checks; it's the skill most exposed to hallucinating a
statute. A curated `.ath/knowledge/legal/` of norms and playbooks gives it a
local, citable source to **read before it asserts** — turning "grounded" from a
promise into a mechanism. The convention is domain-agnostic; only legal-lens is
wired now. Other skills as consumers = parked until value is proven.

## Design (decisions)

Storage — extends the existing `.ath/` namespace:

```
.ath/knowledge/
├── index.md              # optional human-facing catalog (OKF); parked until the KB is large
└── <domain>/<concept>.md # one OKF concept per file, e.g. legal/lgpd-art-7.md
```

File slug — deterministic so the collision edge is enforceable: a concept lives
at `<domain>/<kebab-case(title)>.md` (e.g. title "LGPD art. 7" → `legal/lgpd-art-7.md`).
Same derivation for human- and skill-written entries, so both converge on the
same path for the same concept.

**OKF concept frontmatter** (OKF base + an ath provenance extension; OKF lets
producers add fields and requires consumers to tolerate unknown keys):

```yaml
type: Norma # REQUIRED (OKF). Free string; recommended vocab: Norma | Playbook | Precedente | Checklist
title: LGPD art. 7
description: Legal bases for processing personal data.
resource: https://www.planalto.gov.br/... # URI of the underlying source
tags: [br, lgpd, privacy] # incl. jurisdiction tag so non-BR runs don't misapply
timestamp: 2026-06-22T00:00:00Z
verification: verified # ath: verified | unverified  ← the grounding guarantee
source: human # ath: human | <skill-name>
```

Body uses OKF conventional headings as useful: `# Schema`, `# Examples`,
`# Citations`.

**Curation — skills write, provenance keeps it honest** (the load-bearing call).
Per the chosen model, skills may create entries directly (not only humans). The
safeguard that stops this from poisoning the grounding:

- A skill-written entry is always `verification: unverified`, `source: <skill>`,
  with a `resource` + `# Citations` for where it came from, and a visible
  `> ⚠️ unverified — skill-written lead, confirm before relying on it` banner as
  the first body line. The banner doubles the frontmatter signal so the warning
  survives even if an entry is read or pasted out of its frontmatter context. A
  skill **never** writes `verified` — only a human promotes an entry (drops the
  banner, flips the field) to `verified`.
- Re-writing an existing concept respects provenance: if the file is already
  `verified` (human-trusted), a skill may **only** append to `# Citations` — it
  never touches the frontmatter or body of a verified entry. An `unverified`
  entry it may update (timestamp + citation, staying `unverified`).
- A consumer cites `verified` entries as settled grounding; it treats
  `unverified` entries as **leads to confirm**, never as authority. This is what
  makes "skills write" safe — writes grow the KB fast without contaminating the
  trusted core.

**Retrieval — glob + catalog, LLM picks** (no central registry, no tooling):
the consumer globs `.ath/knowledge/`, reads each file's frontmatter as the
catalog (`type`/`title`/`description`/`tags`/`verification`), the LLM selects the
relevant ones, then reads the bodies of matches and cites `resource` + the doc.
Selection rule (so "relevant" isn't left to vibes): an entry matches only if its
jurisdiction tag matches the resolved jurisdiction **and** its title/description/
tags overlap the artifact's subject; `verified` entries rank above `unverified`
(leads). Scriptless to start; an index-generating script is parked until the KB
is big enough that reading frontmatter across files costs real tokens.

**Read/write ordering — read is a snapshot.** The catalog read (retrieval) is a
single snapshot taken before judging; any entry the lens writes during the run is
for **future** runs and is never cited in the same run that produced it (it's
`unverified` anyway — you don't ground on a lead you just minted). No re-glob
after writing.

**Bootstrap — additive, never required:** `.ath/knowledge/` absent or empty →
the lens behaves exactly as today. The KB only ever adds grounding; it is never
a precondition.

Reuse: the `.ath/` namespace convention, `legal-lens/SKILL.md`, the OKF spec,
frontmatter conventions. The format reference doc + seed entries live with
legal-lens for now (`legal-lens/references/`), moving to a shared home when a
second consumer appears.

Audience: the builder + the team curating legal knowledge. Cut: index/script
tooling, a `/proposed` staging area, a dedicated curation skill, non-legal
consumers — all parked.

## Behavior

**Happy path** (`/ath:legal-lens <slug | path | descrição>`):

1. Resolve jurisdiction (default BR).
2. Before judging, glob `.ath/knowledge/`, read frontmatter as a catalog, select
   entries relevant by type/tags/title/description, read the matched bodies.
3. Ground findings on `verified` entries (cite `resource` + the doc); treat
   `unverified` entries as leads to confirm, not authority.
4. Produce findings (severity + issue-with-solution), citing KB docs where they
   ground a point; flag what still needs a lawyer.
5. If research confirms a norm not yet in the KB, append an OKF concept doc with
   `verification: unverified`, `source: legal-lens`, `resource`, `# Citations`.
6. Report; if the artifact is a shape, append/update `## legal`.

Edge → outcome:

| WHEN                                                          | THEN                                                                                                        |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `.ath/knowledge/` absent or empty                             | lens runs exactly as today; no error (KB is additive)                                                       |
| matched entry is `verification: unverified`                   | cite as a lead to confirm, never as settled law                                                             |
| lens would write an entry it's unsure of                      | write `unverified` + `source: legal-lens` + resource; never `verified`                                      |
| no entry matches the artifact                                 | proceed grounded as today; report findings + note "no KB entry for <topic>" so the gap is visible to curate |
| entry missing required `type` field                           | skip it as malformed; don't fail the run                                                                    |
| jurisdiction is non-BR                                        | select only entries whose tag matches that jurisdiction; never apply a BR-tagged norm to non-BR work        |
| lens discovers a norm mid-run                                 | written as a future-run lead; not cited in the same run (read is a snapshot)                                |
| re-writing a concept whose file is `verified`                 | append to `# Citations` only; never touch the verified entry's frontmatter or body                          |
| re-writing a concept whose file is `unverified`               | update timestamp + append citation, stays `unverified`                                                      |
| writing a concept whose file exists for a _different_ concept | suffix the slug; never overwrite another entry                                                              |

## Tasks

- [x] S1: define the `.ath/knowledge/` OKF convention in a reference doc
      (`legal-lens/references/knowledge-format.md`) — frontmatter + provenance fields,
      `<domain>/<kebab-case(title)>.md` slug rule, the `⚠️ unverified` body banner —
      and seed 1–2 `verified` legal example concepts (e.g. LGPD art. 7 bases). —
      _delivers: the format (slug + banner conventions) + a real catalog to read against_
- [ ] S2: legal-lens **reads** the KB — glob + frontmatter catalog, jurisdiction-
      tag + subject selection rule, snapshot read, reads matches, cites; verified-vs-
      unverified weighting; empty-KB fallback. Edit `legal-lens/SKILL.md`. —
      _delivers: grounded-retrieval happy path + empty-KB / unverified / no-match /
      non-BR / no-entry-match edges_
- [ ] S3: legal-lens **writes** leads — appends `unverified` OKF concepts with
      provenance + banner + citations after research; never writes `verified`;
      verified entries get citation-only appends; slug derivation + collision
      handling. — _delivers: skill-write path + the never-write-verified guard +
      verified-protection + same/different-concept file-collision edges_

## Out of scope

- index.md generation script, `/proposed` staging area, a dedicated curation
  skill, non-legal consumers, vector/semantic retrieval — parked, _revisit_ when
  a second consumer or KB scale justifies it.
- Migrating or importing existing legal content — start curated-empty.

## Open (non-blocking)

- Recommended `type` vocabulary for the legal domain (Norma/Playbook/Precedente/
  Checklist) — refine as real entries accrete. _revisit_
- Whether `verified` promotion needs any tooling beyond a human editing the field
  by hand. _revisit_
