import pytest
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def mongo_client():
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)
    yield client
    client.close()

@pytest.fixture(scope="function")
def test_db(mongo_client):
    db = mongo_client["burguer_app_test"]

    db["users"].delete_many({})  # Limpa a coleção de usuários antes de cada teste
    db["pedidos"].delete_many({})  # Limpa a coleção de pedidos antes de cada teste
   
    yield db