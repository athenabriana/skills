# Product discovery + legal track

## What & why

Expandir a ath para a **frente do diamante** (Discover/Define) + uma **lente
jurídica** — o encaixe real do universo ath numa legaltech. Destila a frente da
Brisa (nise/esperança) em skills finas verb-led, adiciona um revisor de
perspectiva jurídica _grounded_, e unifica o estado sob `.ath/`. Sem personas,
sem router, sem acoplamento Inspira.

A ath hoje é entrega de código (shape→implement→ship). O que falta é a frente:
_descobrir o que vale construir e se aguenta juridicamente_ — exatamente o
trabalho de alto valor na Inspira. nise/esperança já fazem framing de problema e
fit; a lente jurídica é inédita e define o domínio.

## Design (decisions)

Storage — `.ath/` absorve o antigo `.shape/` (só path novo; `.shape/` legado
fica órfão, risco baixo no setup atual):

```
.ath/
├── backlog.md                 # ideias parkeadas repo-wide — consultar sem abrir slug por slug
└── tasks/<slug>/shape.md      # brief por feature, seções acumulam ao longo do fluxo
```

`shape.md` **acumula seções** ao longo do fluxo (um arquivo carrega o contexto
inteiro):

- `## problem` / `## hypothesis` — frame-problem (nise)
- `## fit` / `## cuts` — assess-fit (esperança)
- `## design` / `## behavior` / `## tasks` — shape-idea (existente, Large)
- `## legal` — legal-lens, quando roda contra um shape

Novos skills (verb-led, sem personas, sem router):

- **frame-problem** (de nise): frama o problema antes de solucionar. Captura
  problem statement, hipótese, quem/impacto, métrica de sucesso, appetite.
  Mecanismos: confidence-tag em cada assumption, skip-with-reason, máx 2
  perguntas/turno, echo das respostas. Draft-first. Escreve
  `## problem`/`## hypothesis`. Roda antes da shape-idea e a alimenta.
- **assess-fit** (de esperança): pressiona um problema/ideia framado. Modos:
  market-fit, cuts forçados, priorização, autoria de hipótese testável. Claims
  com evidence-tag. Escreve `## fit`/`## cuts`.
- **legal-lens** (NOVO): lente revisora invocável sobre qualquer artefato
  (ideia, feature, fluxo ou documento). Levanta implicações jurídicas/
  regulatórias, compliance, risco, e o que um advogado exigiria. Jurisdição
  default: **direito brasileiro**, com override. GROUNDED: nunca inventa
  estatuto/precedente, sinaliza incerteza, cita quando dá. Stance (da clarisse):
  só issue significativo, issue-with-solution, severidade blocker/significant/
  minor. Output: reporta na conversa; se o artefato for um shape, adiciona/
  atualiza `## legal`.

shape-idea: core inalterado; passa a **ler** `## problem`/`## hypothesis`/`## fit`
como contexto upstream se presentes. (Não "absorve" mais nise/esperança — elas
viraram verbos standalone.)

Audiência: builder técnico (você + senior). Cortado: personas executive/content,
Framer, e o track de UI (→ backlog).

## Behavior

**frame-problem** happy path:

1. `/ath:frame-problem <descrição>` → sluga a área do problema.
2. Lê codebase/contexto, rascunha `## problem` + `## hypothesis` com palpites,
   cada assumption com confidence-tag.
3. Loop dos gray areas via AskUserQuestion (máx 2/turno), skip-with-reason
   permitido, echo das respostas.
4. Escreve `## problem`/`## hypothesis` em `.ath/tasks/<slug>/shape.md`; aponta
   pra assess-fit ou shape-idea.

**assess-fit** happy path:

1. `/ath:assess-fit <slug>` → lê `## problem`/`## hypothesis`.
2. Escolhe modo (fit / cuts / priorização / hipótese). Rascunha, evidence-tag
   nos claims.
3. Loop dos forks. Escreve `## fit`/`## cuts`.

**legal-lens** happy path:

1. `/ath:legal-lens <slug | path | descrição>` (+ jurisdição opcional).
2. Resolve jurisdição (default BR). Lê o artefato.
3. Produz findings: implicações + risco + exigências-de-advogado, cada um
   issue-with-solution + severidade, incerteza sinalizada.
4. Reporta; se for um shape, adiciona/atualiza `## legal`.

Edge → outcome:

| WHEN                                 | THEN                                            |
| ------------------------------------ | ----------------------------------------------- |
| frame-problem sem slug existente     | cria slug kebab da área do problema             |
| assess-fit sem `## problem` no shape | avisa e sugere rodar frame-problem antes        |
| legal-lens sobre doc fora de `.ath/` | report-only, não escreve seção                  |
| legal-lens incerto sobre a lei       | sinaliza incerteza explicitamente, não inventa  |
| jurisdição não-BR                    | usa a passada; sem hardcode                     |
| assess-fit: claim sem evidência      | tagueia como não-validado, não afirma como fato |
| frame-problem: usuário pula pergunta | registra skip-with-reason, segue                |

## Tasks

- [x] S1: `.ath/` namespace + `backlog.md` — shape-idea escreve
      `.ath/tasks/<slug>/shape.md`; implement-idea/night-shift/ship leem o path novo;
      semeia `backlog.md` com o track de UI parkeado. (foundation) — _delivers:
      migração_
- [x] S2: skill `frame-problem` — problema/hipótese/impacto/métrica/appetite +
      confidence-tag/skip/echo. — _delivers: frame-problem happy path + edges_
- [x] S3: skill `assess-fit` — modos + evidence-tag + cuts/priorização/hipótese.
      — _delivers: assess-fit_
- [x] S4: skill `legal-lens` — revisor grounded, BR-default + override,
      severidade + issue-with-solution, append `## legal`. — _delivers: legal-lens_
- [x] S5: shape-idea lê `## problem`/`## hypothesis`/`## fit` upstream como
      contexto. — _delivers: integração do fluxo_

## Out of scope

- Track de UI (build-ui/review-design/scaffold-app), `.ath/design.md` — parkeado
  em `backlog.md`, _revisit_.
- Personas, router/dispatcher, inspira-install CLI, session.yaml/config.yaml,
  Framer, audiências executive/content — dropados.
- Auto-migração do `.shape/` legado — só path novo.

## Open (não-bloqueante)

- legal-lens análise profunda de documento (contratos/peças) — candidato a
  backlog se a lente provar valor. _revisit_
- formato exato do `backlog.md` — fechar ao semear no S1.
