<<<<<<< HEAD
import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import serialize_user


def test_serialize_user_completo():
    user = {
        "email": "teste@exemplo.com",
        "name": "Teste usuario",
        "address": "Rua Beta",
        "role": "Admin",
    }
    serialized_user = serialize_user(user)
    assert serialized_user == user


def test_serialize_user_vazio():
    user = {
        "email": "teste@exemplo.com",
    }
    serialized_user = serialize_user(user)
    assert serialized_user == {
        "email": "teste@exemplo.com",
        "name": "",
        "address": "",
        "role": "cliente",
    }


def test_serialize_user_vazio():
    user = {}
    serialized_user = serialize_user(user)
    assert serialized_user == {
        "email": None,
        "name": "",
        "address": "",
        "role": "cliente",
    }


def test_serialize_user_inteiro():
    with pytest.raises(AttributeError):
        serialize_user(123)


def test_serialize_user_string():
    with pytest.raises(AttributeError):
        serialize_user("String de teste")


def test_serialize_user_list():
    with pytest.raises(AttributeError):
        serialize_user(["Lista de teste"])


def test_serialize_user_incomun():
    user = {
        "email": 1234,
        "name": ["Teste usuario", "outro teste"],
        "address": {"Rua Beta": "teste de valor inesperado"},
        "role": True,
    }

    serialized_user = serialize_user(user)
    assert serialized_user == {
        "email": 1234,
        "name": ["Teste usuario", "outro teste"],
        "address": {"Rua Beta": "teste de valor inesperado"},
        "role": True,
    }


def test_serialize_user_none():
    with pytest.raises(AttributeError):
        serialize_user(None)


def test_serialize_user_boolean():
    with pytest.raises(AttributeError):
        serialize_user(True)


def test_serialize_user_dict_none():
    user = {
        "email": None,
        "name": None,
        "address": None,
        "role": None,
    }
    serialized_user = serialize_user(user)
    assert serialized_user == {
        "email": None,
        "name": None,
        "address": None,
        "role": None,
    }
=======
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import serialize_user, UserModel

class TestUserModel(unittest.TestCase):

    def setUp(self):
        """Configura o ambiente de teste"""
        self.user_data = UserModel(
            email="teste@exemplo.com",
            name="Test User",
            address="123 Test St",
            role="cliente"
        )

    def tearDown(self):
        """Limpa o ambiente de teste"""
        self.user_data = None

    def test_to_dict(self):
        """Testa a conversão do modelo para dicionário"""
        expected = {
            "email": "teste@exemplo.com",
            "name": "Test User",
            "address": "123 Test St",
            "role": "cliente"
        }
        self.assertEqual(self.user_data.to_dict(), expected)    

    def test_serialize_user_incompleto(self):
       result = self.user_data.serialize()
       self.assertEqual(result["email"], "teste@exemplo.com")
       self.assertEqual(result["name"], "Test User")
       self.assertNotIn("password", result)        


    def test_assert_raises_example(self):

      def raise_error():
          raise ValueError("This is a test error")

      with self.assertRaises(ValueError):
            raise_error()       
>>>>>>> develop
