# Epoch 1 — Gerência de VOD

- **Projeto:** [[PROJECT|Dark Script]] · **Roadmap:** [[ROADMAP|Roadmap]]
- **Status:** concluída
- **Descrição:** Preparar a estrutura de pastas de scripts e entregar os primeiros scripts de gerência de VOD.
- **Yolo:** sim
- **Encerrada em:** 2026-07-27 — todas as tasks concluídas com memory em `pop/memory/` (`1.1.1`, `1.2.1`, `1.2.2`), `develop` integrado em `main` e kanban vazio.

## Recon e forks

- [x] RECON NEEDED: método confiável de detectar faststart sem reprocessar o arquivo — resolvido na 1.2.1: MP4 via trace do ffprobe (moov antes de mdat); MKV via parsing stdlib de cabeçalhos EBML (Cues antes do primeiro Cluster).
- Fork: se os servidores exigirem outra stack além de Python/SH → registrar na phase afetada antes de expandir o scaffold.

## Phase 1.1 — Preparação

- **Status:** concluída
- **Descrição:** Criar o scaffold das pastas de scripts com env, venv, reports e README de listagem.

| Task | Descrição (≤1 linha) | Status |
|------|----------------------|--------|

## Phase 1.2 — Scripts de VOD

- **Status:** concluída
- **Descrição:** Entregar os scripts de gerência da biblioteca VOD, começando pelo diagnóstico de compatibilidade com TVs LG.

| Task | Descrição (≤1 linha) | Status |
|------|----------------------|--------|
