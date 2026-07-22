# Epoch 1 — Gerência de VOD

- **Projeto:** [[PROJECT|Dark Script]] · **Roadmap:** [[ROADMAP|Roadmap]]
- **Status:** em andamento
- **Descrição:** Preparar a estrutura de pastas de scripts e entregar os primeiros scripts de gerência de VOD.
- **Yolo:** sim

## Recon e forks

- [x] RECON NEEDED: método confiável de detectar faststart sem reprocessar o arquivo — resolvido na 1.2.1: MP4 via trace do ffprobe (moov antes de mdat); MKV via parsing stdlib de cabeçalhos EBML (Cues antes do primeiro Cluster).
- Fork: se os servidores exigirem outra stack além de Python/SH → registrar na phase afetada antes de expandir o scaffold.

## Phase 1.1 — Preparação

- **Status:** concluída
- **Descrição:** Criar o scaffold das pastas de scripts com env, venv, reports e README de listagem.

| Task | Descrição (≤1 linha) | Status |
|------|----------------------|--------|

## Phase 1.2 — Scripts de VOD

- **Status:** em andamento
- **Descrição:** Entregar os scripts de gerência da biblioteca VOD, começando pelo diagnóstico de compatibilidade com TVs LG.

| Task | Descrição (≤1 linha) | Status |
|------|----------------------|--------|
| [[1.2.1-script-vod-report-faststart]] | Ler SCAN_VOD_FOLDER, escanear mp4/mkv da pasta e subpastas diretas, detectar arquivos sem flag faststart (que falham em TVs LG) e gerar report MD em reports/ com data YYYYMMDDHHii no nome listando os faltosos. · size: M | 001_initial_task |
