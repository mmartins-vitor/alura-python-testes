import pytest
import requests
from unittest.mock import patch, Mock
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()


# @pytest.fixture(scope="session")
# def mongo_client():
#    uri = os.getenv("MONGO_URI")
#    client = MongoClient(uri)
#    yield client  # o que vier depois serve como ordem de fechamento de conexão
#    client.close()
#
#
# @pytest.fixture(scope="function")
# def test_db(mongo_client):
#    db = mongo_client["burguer_app_test"]
#    db["users"].delete_many({})  # Limpa a coleção de usuários antes de cada teste
#    db["pedidos"].delete_many({})  # Limpa a coleção de pedidos antes de cada teste
#    yield db
#    mongo_client.drop_database("burguer_app_test")
#


@pytest.fixture
def base_urls():
    "Retorna a URL base da aplicação para os testes"
    return {
        "auth_url": "http://127.0.0.1:5000/auth",
        "user_url": "http://127.0.0.1:5001/user",
        "order_url": "http://127.0.0.1:5002/order",
        "product_url": "http://127.0.0.1:5003/product",
    }


@pytest.fixture
def sample_user():
    "Retorna um usuário de exemplo para os testes"
    return {
        "email": "cliente@teste.com",
        "password": "senha123",
        "name": "Cliente teste",
        "address": "Rua teste, 123",
        "role": "cliente",
    }


@pytest.fixture
def sample_items():
    "Retorna os itens de exemplo para os testes"
    return {
        "item_name": ["Hamburguer", "Batata", "Refrigerante"],
        "item_price": [10.0, 5.0, 3.0],
        "quantity": ["2", "1", "1"],
    }


def mock_user_service():
    "mock do serviço de usuário para teste"
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "cliente@teste.com",
            "name": "Cliente teste",
            "address": "Rua teste, 123",
            "role": "cliente",
        }
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_order_service():
    """Mock do serviço de pedidos para testes"""
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {"location": "/order/list"}
        mock_post.return_value = mock_response
        yield mock_post


def chek_service_health(url):
    """Verifica a saúde do serviço"""
    try:
        response = requests.get(f"{url}/", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        return False


@pytest.fixture
def services_running(base_urls):
    """Verifica quais serviços estão rodando"""
    return {service: check_service_health(url) for service, url in base_urls.items()}
