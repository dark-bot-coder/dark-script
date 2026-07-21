# vod-scripts

Scripts da família VOD: gerência da biblioteca de VOD, rodando em servidores externos e enviando dados ao Dark Store.

## Setup

1. Crie o ambiente virtual: `./setup_venv.sh`
2. Ative-o: `source .venv/bin/activate`
3. Copie `.env.example` para `.env` e preencha os valores.

## Scripts

### report_faststart.py

Lista os vídeos `.mp4`/`.mkv` de `SCAN_VOD_FOLDER` (pasta + subpastas diretas) sem o índice no início do arquivo (faststart), gerando um relatório em `reports/`. Requer `ffprobe` no PATH. Somente diagnóstico — nenhum vídeo é alterado.

Uso: `python report_faststart.py` (lê `SCAN_VOD_FOLDER` do ambiente ou do `.env`).
