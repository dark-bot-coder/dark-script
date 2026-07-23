# vod-scripts

Scripts da família VOD: gerência da biblioteca de VOD, rodando em servidores externos e enviando dados ao Dark Store.

## Pré-requisitos

- Python 3
- ffmpeg (`ffmpeg` e `ffprobe` no PATH)
- MKVToolNix (`mkvmerge` no PATH)

## Setup

1. Crie/atualize o ambiente virtual: `./setup_venv.sh`
2. Ative-o: `source .venv/bin/activate`
3. Copie `.env.example` para `.env` e preencha os valores.

## Scripts

### report_faststart.py

Lista os vídeos `.mp4`/`.mkv` de `SCAN_VOD_FOLDER` (pasta + subpastas diretas) sem o índice no início do arquivo (faststart), gerando um relatório em `reports/`. Requer `ffprobe` no PATH. Somente diagnóstico — nenhum vídeo é alterado.

Uso: `python report_faststart.py` (lê `SCAN_VOD_FOLDER` do ambiente ou do `.env`).

### fix_faststart.py

Corrige os vídeos `.mp4`/`.mkv` de `SCAN_VOD_FOLDER` (pasta + subpastas diretas) que não possuem o índice no início (faststart), remuxando o arquivo original.

Modos de execução:

- `python fix_faststart.py` — interativo: pergunta arquivo a arquivo (default `Y`) e cria backup `.bak` antes de corrigir.
- `python fix_faststart.py --yes` — automático: corrige todos sem perguntar e sem backup.
- `python fix_faststart.py --dry-run` — apenas lista o que seria corrigido, sem alterar arquivos.

O script faz verificação embutida; arquivos que já estão corretos são ignorados. Erros de leitura ou correção são salvos em `reports/faststart-fix-errors-YYYYMMDDHHMM.md`.
