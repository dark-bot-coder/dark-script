---
author: agent
created: 2026-07-27
---

# O lote de skills de UI/design/a11y não se aplica ao Dark Script

**Decisão (2026-07-27):** o Dark Script **não** recebe o pacote de skills de frontend, design e acessibilidade que os repos de aplicação com interface mantêm — `ui-change`, `ui-review`, `frontend-design`, `react-best-practices`, `shadcn`, `skill-a11y-audit`, `wcag-accessibility-audit`, `taste-skill`, `impeccable`, `design-tokens`, `color-expert`, `cognitive-walkthrough`, `don-norman-principles-audit`, `nielsen-heuristics-audit`, `ux-audit-rethink`, `ui-design-review`, `web-artifacts-builder`, `web-design-guidelines`. A ausência delas em `.agents/skills/` **não é drift** e não deve ser reaberta como pendência em revisões futuras.

## Evidência

- **Ficha e objetivo** ([[PROJECT|Dark Script]]): "scripts de organização externa do Dark Store — utilitários que rodam em servidores próprios e enviam dados à plataforma dark-store". Nenhuma interface de usuário no escopo.
- **Conteúdo do repo (2026-07-27):** só `vod-scripts/`, `creed-scripts/`, `bin-scripts/` e `office-scripts/` com `.env.example`, `setup_venv.sh`, `README.md` e scripts Python de CLI. Zero arquivo `.html`, `.css`, `.ts/.tsx`, `.vue`, `.svelte` ou `package.json`.
- **Superfície de saída:** relatórios markdown em `reports/` e logs de terminal — sem render visual, sem TUI, sem servidor HTTP servindo página.
- **Roadmap** ([[ROADMAP|Roadmap]]): Epoch 1 entregou scaffold e scripts de VOD; a única ideia futura registrada é o contrato de **envio de dados** ao dark-store (cliente HTTP), que segue sem UI.

## Consequências

- O lote de skills relevante aqui é o de código (`clean-code-change` / `clean-code-review`), já instalado.
- Se algum dia nascer superfície visual neste repo (dashboard, página de relatório, TUI), esta decisão deve ser revisitada — e a instalação das skills é operação do **PoP raiz**, nunca feita de dentro deste repo.
