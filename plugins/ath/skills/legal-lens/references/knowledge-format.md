# Knowledge format — `.ath/knowledge/` (OKF)

A repo-local, git-committed knowledge base the legal lens reads before it
asserts, so "grounded" is a mechanism and not a promise. It follows
[OKF](https://okf.md/spec/) (Open Knowledge Format): a directory of markdown
files, each with YAML frontmatter and one required field `type`. This base is
distinct from Claude Code's per-user memory — it's team knowledge that travels
with the repo.

## Layout

```
.ath/knowledge/
├── index.md              # optional human-facing catalog; skip until the base is large
└── <domain>/<slug>.md    # one concept per file, e.g. legal/lgpd-art-7.md
```

`<slug>` is `kebab-case(title)`, so the same concept resolves to the same path
whoever writes it (`title: "LGPD art. 7"` → `legal/lgpd-art-7.md`). This is what
makes the collision rule enforceable: same concept → same file; a genuinely
different concept that would collide gets a suffix (`-2`), never an overwrite.

## Frontmatter

OKF base fields plus an `ath` provenance extension. OKF lets producers add
fields and requires consumers to tolerate unknown keys, so the extension is
spec-compliant.

```yaml
type: Norma # REQUIRED (OKF). Free string; legal vocab: Norma | Playbook | Precedente | Checklist
title: LGPD art. 7
description: Legal bases for processing personal data under the LGPD.
resource: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
tags: [br, lgpd, privacy] # include the jurisdiction tag so non-BR runs don't misapply it
timestamp: 2026-06-22T00:00:00Z
verification: verified # ath: verified | unverified  ← the grounding guarantee
source: human # ath: human | <skill-name>
```

Body uses OKF conventional headings where useful: `# Schema`, `# Examples`,
`# Citations`.

## Provenance — the grounding guarantee

The base stays trustworthy because two fields gate how it's read and written:

- **`verification: verified`** — a human vouched for it. A consumer cites it as
  settled grounding.
- **`verification: unverified`** — a skill researched and wrote it. A consumer
  treats it as a **lead to confirm**, never as authority. Unverified entries
  also carry a visible banner as their first body line, so the warning survives
  being read or pasted out of frontmatter context:

  ```
  > ⚠️ unverified — skill-written lead, confirm before relying on it
  ```

A skill only ever writes `unverified` / `source: <skill-name>`. Promotion to
`verified` is a human action: drop the banner, flip the field, set
`source: human`. Re-writing respects this — a skill that re-discovers a
`verified` concept appends to `# Citations` only and leaves the frontmatter and
body untouched; an `unverified` concept it may refresh (new timestamp + citation,
staying `unverified`).

## Example concept (verified)

`legal/lgpd-art-7.md`:

```markdown
---
type: Norma
title: LGPD art. 7
description: The ten legal bases that authorize processing of personal data.
resource: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
tags: [br, lgpd, privacy, legal-basis]
timestamp: 2026-06-22T00:00:00Z
verification: verified
source: human
---

# Schema

Processing of personal data is lawful only under one of the ten bases in
art. 7 — consent, legal obligation, contract, legitimate interest, and others.
Consent (inc. I) is one basis among ten, not the default; picking the right
basis is the design decision, and legitimate interest (inc. IX) carries its own
balancing-test duty.

# Examples

- A signup flow storing an email to deliver the service → contract (inc. V),
  not consent.
- Sending marketing to that email → consent (inc. I) or legitimate interest
  (inc. IX) with a balancing test on file.

# Citations

- Lei nº 13.709/2018 (LGPD), art. 7.
```

## Example concept (unverified, skill-written)

`legal/marco-civil-data-retention.md`:

```markdown
---
type: Norma
title: Marco Civil data retention
description: Connection and access logs retention duties for internet providers.
resource: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm
tags: [br, marco-civil, logs, retention]
timestamp: 2026-06-22T00:00:00Z
verification: unverified
source: legal-lens
---

> ⚠️ unverified — skill-written lead, confirm before relying on it

# Schema

Marco Civil da Internet sets log-retention windows for connection providers and
application providers. The exact windows and which provider class a given system
falls into need a lawyer's confirmation before they ground a launch decision.

# Citations

- Lei nº 12.965/2014 (Marco Civil), arts. 13–15 — to confirm.
```
