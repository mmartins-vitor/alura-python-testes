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
            role="cliente",
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
            "role": "cliente",
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
