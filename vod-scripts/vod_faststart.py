#!/usr/bin/env python3
"""Funções compartilhadas para detecção de faststart em vídeos VOD.

Módulo reutilizado pelos scripts de relatório e correção de faststart.
"""

import os
import re
import subprocess
from pathlib import Path

PASTA_SCRIPT = Path(__file__).resolve().parent
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
    """Lê variáveis de ambiente do arquivo .env do script, se existir."""
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
    """Lista arquivos .mp4/.mkv da pasta raiz e de suas subpastas diretas."""
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
    """Retorna True se o MP4 tem o átomo moov antes do mdat (faststart)."""
    try:
        resultado = subprocess.run(
            ["ffprobe", "-v", "trace", "-read_intervals", "0%+#1", str(caminho)],
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        raise ErroLeitura("ffprobe excedeu o tempo limite de 60s")
    if resultado.returncode != 0:
        raise ErroLeitura("ffprobe não conseguiu ler o arquivo")
    boxes = LINHA_BOX_RAIZ.findall(resultado.stderr)
    if "moov" not in boxes or "mdat" not in boxes:
        raise ErroLeitura("boxes moov/mdat não encontrados")
    return boxes.index("moov") < boxes.index("mdat")


def _ler_byte(arq):
    byte = arq.read(1)
    if not byte:
        raise ErroLeitura("fim inesperado no cabeçalho EBML")
    return byte[0]


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
        valor = (valor << 8) | _ler_byte(arq)
    return valor


def _ler_tamanho_ebml(arq):
    primeiro = _ler_byte(arq)
    mascara, tamanho = 0x80, 1
    while tamanho <= 8 and not (primeiro & mascara):
        mascara >>= 1
        tamanho += 1
    if tamanho > 8:
        raise ErroLeitura("tamanho EBML inválido")
    valor = primeiro & (mascara - 1)
    for _ in range(tamanho - 1):
        valor = (valor << 8) | _ler_byte(arq)
    if valor == (1 << (7 * tamanho)) - 1:
        return None
    return valor


def mkv_tem_faststart(caminho):
    """Retorna True se o MKV tem Cues antes do primeiro Cluster."""
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
    """Detecta se o vídeo (MP4 ou MKV) possui o índice no início."""
    if caminho.suffix.lower() == ".mp4":
        return mp4_tem_faststart(caminho)
    return mkv_tem_faststart(caminho)
