# ath backlog — ideias parkeadas

Parking repo-wide pra boas ideias adiadas de trabalho já shapeado. Consultar aqui
em vez de abrir slug por slug. Cada item marcado *revisit* foi cortado de um
shape consciente, não esquecido.

## UI build track (da Brisa: tarsila/clarisse/brisar) — *revisit*

Engavetado em favor do track discovery+jurídico (ver
`tasks/discovery-legal-track/shape.md`). Distilação já desenhada:

- **build-ui** (de tarsila) — gera tela/componente real; **sempre detecta o
  stack** (sem framework predefinido); lê `.ath/design.md` + seção `## ui` do
  shape + o código real; faz bootstrap do `design.md` na 1ª run se faltar;
  estados Loading/Empty/Error sempre; roda typecheck/build do projeto se existir.
  `design.md` vira read-only pós-criação — nunca inventa token, sinaliza
  faltante.
- **review-design** (clarisse + /ui-accessibility) — revisa tela construída vs a
  intenção do `## ui` + auditoria WCAG AA; severidade + issue-with-solution; só
  issue significativo.
- **scaffold-app** (brisar, distilado) — bootstrapa um surface de produto,
  estabelece o DS → `.ath/design.md`. Sem inspira-install CLI, sem personas, sem
  session.yaml.

Contratos já decididos pra quando voltar:

- `.ath/design.md` (DS compartilhado, repo-wide) — seções: `## tokens` /
  `## components` / `## brand & voice` / `## layout` / `## direction`.
- `## ui` = seção no `shape.md` com a intenção visual da tela (qualquer tamanho,
  não só Large). build-ui lê; se ausente, cai no `design.md` genérico.
- **build-ui render-verify** — script que renderiza um componente isolado + tira
  screenshot, sem subir o app inteiro. Fecha o loop de verificação que o v1
  deixa cego.

## legal-lens extensions

- Análise profunda de documento jurídico (contratos, peças) — adjacente ao
  LexFlow. Candidato se a lente revisora provar valor.
