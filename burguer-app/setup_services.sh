for svc in "${services[@]}"; do
  if [[ -d "$svc" ]]; then
    if [[ -d "$svc/.venv" ]]; then
      echo "⚠️  Já existe: $svc/.venv"
    else
      echo "📦 Criando venv em $svc/.venv"
      "$PYTHON_BIN" -m venv "$svc/.venv"
      echo "✅ Feito: $svc/.venv"
    fi

    # Ativa o venv e instala dependências
    source "$svc/.venv/bin/activate"
    pip install --upgrade pip
    pip install python-dotenv

    if [[ -f "$svc/requirements.txt" ]]; then
      pip install -r "$svc/requirements.txt"
    else
      echo "⚠️  $svc não tem requirements.txt"
    fi
    deactivate

    # Cria .env se não existir
    if [[ ! -f "$svc/.env" ]]; then
      cat > "$svc/.env" <<'EOF'
appName=Alura
MONGO_URI=mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/dbname
SECRET_KEY=alura-secret-key
EOF
      echo "✅ Criado $svc/.env"
    fi

    # Garante que .env está no .gitignore
    if [[ ! -f "$svc/.gitignore" ]] || ! grep -qxF ".env" "$svc/.gitignore"; then
      echo ".env" >> "$svc/.gitignore"
      echo "📄 Adicionado '.env' ao $svc/.gitignore"
    fi
  else
    echo "⛔ Diretório não encontrado: $svc (ignorando)"
  fi
done
