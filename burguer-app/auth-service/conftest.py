import pytest
import requests
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

@pytest.fixture
def base_urls():
    """URLs base dos serviços"""
    return {
        "order": "http://localhost:5002/order",
        "user": "http://localhost:5001/user",
        "product_url": "http://localhost:5003/product",
        "auth_url": "http://localhost:5000/auth"
    }

@pytest.fixture
def sample_user():
    """Dados de usuário existente"""
    return {
        "email": "cliente@teste.com",
        "password": "123456",
        "name": "Cliente Teste",
        "address": "Rua Fictícia, 123",
        "role": "cliente"
    }

@pytest.fixture
def sample_items():
    """Itens de pedido simulados"""
    return {
        "item_name": ["X-Burger", "Coca-Cola"],
        "item_quantity": ["2", "1"],
        "item_price": ["25.00", "5.90"]
    }

@pytest.fixture
def mock_user_service():
    """Mock do user service para testes unitários"""
    with patch('requests.get') as mock_get:
        # Simula resposta do user service
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "cliente@teste.com",
            "name": "Cliente Teste",
            "role": "cliente"
        }
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_order_service():
    """Mock do order service para testes unitários"""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {'Location': '/order/list'}
        mock_post.return_value = mock_response
        yield mock_post

def check_service_health(url):
    """Verifica se um serviço está rodando"""
    try:
        response = requests.get(f"{url}/", timeout=2)
        return response.status_code in [200, 302, 404]  # 404 é OK, significa que está rodando
    except requests.exceptions.ConnectionError:
        return False

@pytest.fixture
def services_running(base_urls):
    """Verifica quais serviços estão rodando"""
    return {
        service: check_service_health(url) 
        for service, url in base_urls.items()
    }

@pytest.fixture
def skip_if_services_down(services_running):
    """Pula testes se os serviços não estiverem rodando"""
    def _skip_if_down(*required_services):
        for service in required_services:
            if not services_running.get(f"{service}_url", False):
                pytest.skip(f"Serviço {service} não está rodando")
    return _skip_if_down
