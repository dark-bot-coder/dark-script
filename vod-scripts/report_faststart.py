#!/usr/bin/env python3
"""Gera relatório dos vídeos sem faststart (índice no início) da pasta SCAN_VOD_FOLDER.

Somente diagnóstico: nenhum arquivo de vídeo é alterado.
Exit codes: 0 em execução normal (mesmo com faltosos); 2 em falha operacional.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from vod_faststart import (
    ErroLeitura,
    analisar_video,
    carregar_env_local,
    varrer_videos,
)

PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_REPORTS = PASTA_SCRIPT / "reports"


def gerar_relatorio(raiz, ok, faltosos, erros):
    agora = datetime.now()
    linhas = [
        "# Relatório de faststart",
        "",
        f"- **Data:** {agora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Pasta escaneada:** {raiz}",
        "",
        "## Totais",
        "",
        f"- Escaneados: {len(ok) + len(faltosos) + len(erros)}",
        f"- OK (índice no início): {len(ok)}",
        f"- Faltosos (sem índice no início): {len(faltosos)}",
        f"- Erros de leitura: {len(erros)}",
        "",
        "## Faltosos (sem índice no início)",
        "",
    ]
    if faltosos:
        linhas += [f"- `{caminho}`" for caminho in faltosos]
    else:
        linhas.append("Nenhum.")
    linhas += ["", "## Erros de leitura", ""]
    if erros:
        linhas += [f"- `{caminho}` — {motivo}" for caminho, motivo in erros]
    else:
        linhas.append("Nenhum.")
    linhas.append("")

    PASTA_REPORTS.mkdir(exist_ok=True)
    destino = PASTA_REPORTS / f"faststart-report-{agora.strftime('%Y%m%d%H%M')}.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    return destino


def main():
    carregar_env_local()

    pasta = os.environ.get("SCAN_VOD_FOLDER", "").strip()
    if not pasta:
        print(
            "Erro: SCAN_VOD_FOLDER não definida ou vazia. "
            "Defina-a no ambiente ou no arquivo .env.",
            file=sys.stderr,
        )
        return 2
    raiz = Path(pasta)
    if not raiz.is_dir():
        print(f"Erro: pasta não encontrada ou sem permissão de leitura: {raiz}", file=sys.stderr)
        return 2
    if shutil.which("ffprobe") is None:
        print("Erro: ffprobe não encontrado no PATH. Instale o pacote ffmpeg.", file=sys.stderr)
        return 2

    print(f"Varrendo pasta: {raiz}")
    videos = varrer_videos(raiz)
    print(f"Vídeos encontrados: {len(videos)}")

    ok, faltosos, erros = [], [], []
    for video in videos:
        relativo = video.relative_to(raiz)
        try:
            if analisar_video(video):
                ok.append(str(relativo))
                print(f"OK: {relativo}")
            else:
                faltosos.append(str(relativo))
                print(f"Sem faststart: {relativo}")
        except ErroLeitura as exc:
            erros.append((str(relativo), str(exc)))
            print(f"Erro de leitura: {relativo} ({exc})")

    destino = gerar_relatorio(raiz, ok, faltosos, erros)
    print(
        f"Resumo: {len(ok)} ok, {len(faltosos)} faltosos, "
        f"{len(erros)} erros de leitura."
    )
    print(f"Relatório salvo em: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
