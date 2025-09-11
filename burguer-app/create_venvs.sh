#!/usr/bin/env bash
# Cria um .venv em cada microsserviço (Linux/WSL)
# Serviços: auth-service, order-service, product-service, user-service

set -euo pipefail

PYTHON_BIN="${PYTHON:-python3}"
services=(auth-service order-service product-service user-service)

for svc in "${services[@]}"; do
  if [[ -d "$svc" ]]; then
    if [[ -d "$svc/.venv" ]]; then
      echo "⚠️  Já existe: $svc/.venv"
    else
      echo "📦 Criando venv em $svc/.venv"
      "$PYTHON_BIN" -m venv "$svc/.venv"
      echo "✅ Feito: $svc/.venv"
    fi
  else
    echo "⛔ Diretório não encontrado: $svc (ignorando)"
  fi
done
