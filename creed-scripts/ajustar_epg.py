#!/usr/bin/env python3
"""Ajusta os horários (start/stop) de um arquivo XMLTV, gerando uma cópia corrigida."""

import argparse
import re
from datetime import datetime, timedelta

TIMESTAMP_RE = re.compile(r'(start|stop)="(\d{14}) ([+-]\d{4})"')


def ajustar(entrada, saida, horas):
    delta = timedelta(hours=horas)
    total = 0

    def substituir(match):
        nonlocal total
        atributo, ts, offset = match.groups()
        novo = datetime.strptime(ts, "%Y%m%d%H%M%S") + delta
        total += 1
        return f'{atributo}="{novo:%Y%m%d%H%M%S} {offset}"'

    with open(entrada, "r", encoding="utf-8", newline="") as fin, \
         open(saida, "w", encoding="utf-8", newline="") as fout:
        for linha in fin:
            fout.write(TIMESTAMP_RE.sub(substituir, linha))

    print(f"{total} timestamps ajustados em {horas:+g}h -> {saida}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", nargs="?", default="epg.xml")
    parser.add_argument("saida", nargs="?", default="epg_ajustado.xml")
    parser.add_argument("--horas", type=float, default=-3,
                        help="horas a somar aos horários (padrão: -3)")
    args = parser.parse_args()
    ajustar(args.entrada, args.saida, args.horas)


if __name__ == "__main__":
    main()
