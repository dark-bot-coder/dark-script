# dark-script

Scripts de organização externa do **Dark Store**: rodam em servidores próprios e enviam dados à plataforma dark-store.

## Estrutura

- `bin-scripts/` — utilitários gerais de manutenção.
- `creed-scripts/` — scripts do Creed (ex.: ajuste de EPG).
- `office-scripts/` — scripts administrativos/office.
- `vod-scripts/` — tratamento de VOD (ex.: faststart de vídeos).

Cada pasta tem `setup_venv.sh` para preparar o ambiente Python e `reports/` para saídas.

## Harness

Projeto uni-repo gerido pelo workflow **ProjectOfProjects (PoP)**: regras para agentes em `AGENTS.md`, harness completo em `pop/` (roadmap, kanban, specs, skills).
