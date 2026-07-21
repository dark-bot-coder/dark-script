#!/usr/bin/env python3
"""Gera relatório dos vídeos sem faststart (índice no início) da pasta SCAN_VOD_FOLDER.

Somente diagnóstico: nenhum arquivo de vídeo é alterado.
Exit codes: 0 em execução normal (mesmo com faltosos); 2 em falha operacional.
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_REPORTS = PASTA_SCRIPT / "reports"
EXTENSOES_VIDEO = {".mp4", ".mkv"}

LINHA_BOX_RAIZ = re.compile(r"type:'(\w+)' parent:'root'")

# Elementos EBML (matroska) inspecionados no cabeçalho do arquivo.
ID_EBML = 0x1A45DFA3
ID_SEGMENTO = 0x18538067
ID_CUES = 0x1C53BB6B
ID_CLUSTER = 0x1F43B675


class ErroLeitura(Exception):
    """Falha ao ler ou interpretar um vídeo; o arquivo vai para a seção de erros."""


def carregar_env_local():
    caminho_env = PASTA_SCRIPT / ".env"
    if not caminho_env.is_file():
        return
    for linha in caminho_env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


def varrer_videos(raiz):
    videos = []
    for entrada in sorted(raiz.iterdir()):
        if entrada.is_file() and entrada.suffix.lower() in EXTENSOES_VIDEO:
            videos.append(entrada)
        elif entrada.is_dir():
            for sub in sorted(entrada.iterdir()):
                if sub.is_file() and sub.suffix.lower() in EXTENSOES_VIDEO:
                    videos.append(sub)
    return videos


def mp4_tem_faststart(caminho):
    resultado = subprocess.run(
        ["ffprobe", "-v", "trace", "-read_intervals", "0%+#1", str(caminho)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if resultado.returncode != 0:
        raise ErroLeitura("ffprobe não conseguiu ler o arquivo")
    boxes = LINHA_BOX_RAIZ.findall(resultado.stderr)
    if "moov" not in boxes or "mdat" not in boxes:
        raise ErroLeitura("boxes moov/mdat não encontrados")
    return boxes.index("moov") < boxes.index("mdat")


def _ler_id_ebml(arq):
    primeiro = arq.read(1)
    if not primeiro:
        return None
    mascara, tamanho = 0x80, 1
    while tamanho <= 4 and not (primeiro[0] & mascara):
        mascara >>= 1
        tamanho += 1
    if tamanho > 4:
        raise ErroLeitura("ID EBML inválido")
    valor = primeiro[0]
    for _ in range(tamanho - 1):
        valor = (valor << 8) | arq.read(1)[0]
    return valor


def _ler_tamanho_ebml(arq):
    primeiro = arq.read(1)
    if not primeiro:
        raise ErroLeitura("fim inesperado no cabeçalho EBML")
    mascara, tamanho = 0x80, 1
    while tamanho <= 8 and not (primeiro[0] & mascara):
        mascara >>= 1
        tamanho += 1
    if tamanho > 8:
        raise ErroLeitura("tamanho EBML inválido")
    valor = primeiro[0] & (mascara - 1)
    for _ in range(tamanho - 1):
        valor = (valor << 8) | arq.read(1)[0]
    if valor == (1 << (7 * tamanho)) - 1:
        return None
    return valor


def mkv_tem_faststart(caminho):
    # O trace do ffprobe não expõe elementos EBML, então o cabeçalho é lido
    # diretamente: Cues (índice) deve vir antes do primeiro Cluster.
    with open(caminho, "rb") as arq:
        if _ler_id_ebml(arq) != ID_EBML:
            raise ErroLeitura("cabeçalho EBML não encontrado")
        tamanho = _ler_tamanho_ebml(arq)
        arq.seek(tamanho, 1)
        if _ler_id_ebml(arq) != ID_SEGMENTO:
            raise ErroLeitura("segmento EBML não encontrado")
        _ler_tamanho_ebml(arq)
        pos_cues = None
        while True:
            posicao = arq.tell()
            id_elemento = _ler_id_ebml(arq)
            if id_elemento is None:
                break
            tamanho = _ler_tamanho_ebml(arq)
            if id_elemento == ID_CLUSTER:
                return pos_cues is not None and pos_cues < posicao
            if id_elemento == ID_CUES:
                pos_cues = posicao
            if tamanho is None:
                raise ErroLeitura("elemento EBML de tamanho desconhecido")
            arq.seek(tamanho, 1)
        raise ErroLeitura("nenhum Cluster encontrado")


def analisar_video(caminho):
    if caminho.suffix.lower() == ".mp4":
        return mp4_tem_faststart(caminho)
    return mkv_tem_faststart(caminho)


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
