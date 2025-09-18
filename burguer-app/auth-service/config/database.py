"""
Conecta ao  banco de dados MongoDB utilizando as variáveis de ambiente
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env

load_dotenv()

# Cria a conexão com o banco de dados MongoDB

client = MongoClient(os.getenv("MONGO_URI"))

# Seleciona o banco de dados
db = client["burguer_app_db"]


def get_db():
    """Função para retornar a instância do banco de dados"""
    return db
