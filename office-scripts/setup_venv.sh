#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
    echo "Erro: python3 não encontrado. Instale o Python 3 antes de continuar." >&2
    exit 1
fi

if [ ! -d .venv ]; then
    echo "Criando ambiente virtual em .venv ..."
    python3 -m venv .venv
else
    echo "Ambiente virtual .venv já existe; reutilizando."
fi

echo "Atualizando pip ..."
.venv/bin/pip install --upgrade pip --quiet

if [ -f requirements.txt ]; then
    echo "Instalando dependências de requirements.txt ..."
    .venv/bin/pip install -r requirements.txt
else
    echo "Nenhum requirements.txt encontrado; nenhuma dependência instalada."
fi

echo "Verificando instalação ..."
.venv/bin/python --version

echo ""
echo "Ambiente pronto. Para ativá-lo, rode:"
echo "  source .venv/bin/activate"
