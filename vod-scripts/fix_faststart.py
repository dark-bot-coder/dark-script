#!/usr/bin/env python3
"""Corrige vídeos sem faststart (índice no início) da pasta SCAN_VOD_FOLDER.

Modos de execução:
- Interativo (padrão): pergunta arquivo a arquivo, default Y, cria backup .bak.
- --yes: corrige todos sem perguntar e sem backup.
- --dry-run: apenas lista o que seria corrigido, sem alterar arquivos.

O script faz verificação embutida; arquivos já corretos são ignorados.
Exit codes: 0 em execução normal (mesmo com erros de correção); 2 em falha operacional.
"""

import argparse
import os
import shutil
import subprocess
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


class ErroCorrecao(Exception):
    """Falha ao corrigir um vídeo; o arquivo vai para o relatório de erros."""


def caminho_temporario(caminho):
    """Retorna o caminho do arquivo temporário de correção.

    Usa o sufixo original (.mp4/.mkv) para que ffmpeg/mkvmerge identifiquem o
    formato, mantendo o marcador .tmp no nome.
    """
    return caminho.with_name(f"{caminho.stem}.tmp{caminho.suffix}")


def caminho_backup(caminho):
    """Retorna o caminho do arquivo de backup."""
    return caminho.with_name(caminho.name + ".bak")


def exigir_ferramentas():
    """Verifica se ffmpeg e ffprobe estão disponíveis no PATH.

    mkvmerge é necessário apenas para correção de MKV e é verificado no momento
    do uso.
    """
    faltantes = [nome for nome in ("ffmpeg", "ffprobe") if shutil.which(nome) is None]
    if faltantes:
        raise RuntimeError(f"ferramentas não encontradas no PATH: {', '.join(faltantes)}")


def remover_se_existir(caminho):
    """Remove um arquivo se ele existir; usado para limpar temporários."""
    try:
        if caminho.is_file():
            caminho.unlink()
    except OSError as exc:
        raise ErroCorrecao(f"não conseguiu remover arquivo existente: {exc}") from exc


def corrigir_mp4(caminho, destino):
    """Remuxa um MP4 com -movflags +faststart no destino."""
    remover_se_existir(destino)
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(caminho),
        "-c",
        "copy",
        "-movflags",
        "+faststart",
        str(destino),
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise ErroCorrecao(f"ffmpeg falhou: {stderr}") from exc
    except FileNotFoundError as exc:
        raise ErroCorrecao("ffmpeg não encontrado") from exc


def corrigir_mkv(caminho, destino):
    """Remuxa um MKV com mkvmerge no destino. Retorna True se houve warnings."""
    remover_se_existir(destino)
    cmd = ["mkvmerge", "-o", str(destino), str(caminho)]
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError as exc:
        raise ErroCorrecao("mkvmerge não encontrado") from exc
    if resultado.returncode not in (0, 1):
        stdout = (resultado.stdout or "").strip()
        stderr = (resultado.stderr or "").strip()
        raise ErroCorrecao(
            f"mkvmerge falhou (rc={resultado.returncode}): {stdout} {stderr}"
        )
    return resultado.returncode == 1


def verificar_pos_correcao(caminho):
    """Confirma se o arquivo temporário realmente ficou com faststart."""
    try:
        if not analisar_video(caminho):
            raise ErroCorrecao("arquivo corrigido ainda não possui faststart")
    except ErroLeitura as exc:
        raise ErroCorrecao(f"não conseguiu verificar correção: {exc}") from exc


def substituir_atomicamente(original, temporario, fazer_backup):
    """Move o temporário para o lugar do original, opcionalmente criando backup."""
    try:
        shutil.copymode(original, temporario)
    except OSError as exc:
        raise ErroCorrecao(f"não conseguiu copiar permissões: {exc}") from exc

    backup = None
    if fazer_backup:
        backup = caminho_backup(original)
        if backup.exists():
            raise ErroCorrecao(f"arquivo de backup já existe: {backup}")
        try:
            os.replace(original, backup)
        except OSError as exc:
            raise ErroCorrecao(f"não conseguiu criar backup: {exc}") from exc

    try:
        os.replace(temporario, original)
    except OSError as exc:
        if backup is not None:
            try:
                os.replace(backup, original)
            except OSError as restore_exc:
                raise ErroCorrecao(
                    f"não conseguiu substituir arquivo original ({exc}); "
                    f"backup em {backup} não pôde ser restaurado: {restore_exc}"
                ) from exc
        raise ErroCorrecao(f"não conseguiu substituir arquivo original: {exc}") from exc


def confirmar(caminho_relativo):
    """Pergunta ao usuário se deseja corrigir o arquivo. Retorna True/False."""
    while True:
        resposta = input(f"Corrigir {caminho_relativo}? [Y/n/q] ").strip().lower()
        if resposta in ("", "y", "yes", "s", "sim"):
            return True
        if resposta in ("n", "no", "nao", "não"):
            return False
        if resposta in ("q", "quit"):
            raise KeyboardInterrupt
        print("Resposta inválida. Digite Y, n ou q.")


def corrigir_video(caminho, relativo, modo_auto, dry_run, fazer_backup):
    """Verifica e, se necessário, corrige um único vídeo.

    Retorna uma string indicando o resultado: 'ok', 'corrigido', 'ignorado'
    ou 'dry_run'.
    """
    try:
        tem_faststart = analisar_video(caminho)
    except ErroLeitura as exc:
        raise ErroCorrecao(f"erro de leitura: {exc}") from exc

    if tem_faststart:
        print(f"Já ok: {relativo}")
        return "ok"

    if dry_run:
        print(f"Seria corrigido: {relativo}")
        return "dry_run"

    if not modo_auto:
        if not confirmar(relativo):
            print(f"Ignorado: {relativo}")
            return "ignorado"

    temporario = caminho_temporario(caminho)
    try:
        if caminho.suffix.lower() == ".mp4":
            aviso = corrigir_mp4(caminho, temporario)
        else:
            aviso = corrigir_mkv(caminho, temporario)

        verificar_pos_correcao(temporario)
        substituir_atomicamente(caminho, temporario, fazer_backup)

        if aviso:
            print(f"Corrigido com aviso: {relativo}")
        else:
            print(f"Corrigido: {relativo}")
        return "corrigido"
    except Exception:
        remover_se_existir(temporario)
        raise


def gerar_relatorio_erros(raiz, erros):
    """Gera relatório apenas com os erros encontrados."""
    agora = datetime.now()
    linhas = [
        "# Relatório de erros — correção de faststart",
        "",
        f"- **Data:** {agora.strftime('%Y-%m-%d %H:%M')}",
        f"- **Pasta escaneada:** {raiz}",
        f"- **Total de erros:** {len(erros)}",
        "",
        "## Erros",
        "",
    ]
    linhas += [f"- `{caminho}` — {motivo}" for caminho, motivo in erros]
    linhas.append("")

    PASTA_REPORTS.mkdir(exist_ok=True)
    destino = PASTA_REPORTS / f"faststart-fix-errors-{agora.strftime('%Y%m%d%H%M')}.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    return destino


def main():
    parser = argparse.ArgumentParser(
        description="Corrige vídeos sem faststart em SCAN_VOD_FOLDER."
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="corrige todos sem perguntar e sem criar backup",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="apenas lista o que seria corrigido, sem alterar arquivos",
    )
    args = parser.parse_args()

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
        print(
            f"Erro: pasta não encontrada ou sem permissão de leitura: {raiz}",
            file=sys.stderr,
        )
        return 2

    try:
        exigir_ferramentas()
    except RuntimeError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 2

    print(f"Varrendo pasta: {raiz}")
    if args.dry_run:
        print("Modo dry-run: nenhum arquivo será alterado.")
    videos = varrer_videos(raiz)
    print(f"Vídeos encontrados: {len(videos)}")

    erros = []
    contador = {"ok": 0, "corrigido": 0, "ignorado": 0, "dry_run": 0}

    for video in videos:
        relativo = video.relative_to(raiz)
        try:
            resultado = corrigir_video(
                caminho=video,
                relativo=relativo,
                modo_auto=args.yes,
                dry_run=args.dry_run,
                fazer_backup=not args.yes and not args.dry_run,
            )
            contador[resultado] += 1
        except (ErroCorrecao, ErroLeitura) as exc:
            erros.append((str(relativo), str(exc)))
            print(f"Erro: {relativo} ({exc})")
        except KeyboardInterrupt:
            print("\nInterrompido pelo usuário.")
            break

    if erros:
        destino = gerar_relatorio_erros(raiz, erros)
        print(f"Relatório de erros salvo em: {destino}")

    print(
        f"Resumo: {contador['ok']} ok, {contador['corrigido']} corrigidos, "
        f"{contador['ignorado']} ignorados, {len(erros)} erros."
    )
    if args.dry_run:
        print(f"Seriam corrigidos (dry-run): {contador['dry_run']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
