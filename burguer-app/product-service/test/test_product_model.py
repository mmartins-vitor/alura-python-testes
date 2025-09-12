import pytest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.product_model import serialize_product

from bson.objectid import ObjectId


# Retorna todos os campos esperados corretamente.
def test_serialize_product_completo():
    product = {
        "_id": "1",  # chave corrigida
        "name": "cerveja",
        "description": "skol",
        "category": "bebida",
        "price": 10.9,  # de preferência número
        "available": True,
        "ingredients": ["lupulo", "cevada", "agua"],
    }
    serialized_product = serialize_product(product)
    expected = {
        "id": "1",
        "name": "cerveja",
        "description": "skol",
        "category": "bebida",
        "price": 10.9,
        "available": True,
        "ingredients": ["lupulo", "cevada", "agua"],
    }
    assert serialized_product == expected


# Aplica os valores padrão para os campos opcionais (available e ingredients).
def test_serialize_product_padrao_available():
    product = {"_id": 2, "name": "coca-cola"}
    serialized_product = serialize_product(product)
    expected = {
        "id": "2",
        "name": "coca-cola",
        "description": None,  # porque não existe a chave
        "category": None,  # idem
        "price": None,  # idem
        "available": True,  # valor padrão definido
        "ingredients": [],  # valor padrão definido
    }
    assert serialized_product == expected


# Converte corretamente o campo _id para uma string.
def test_serialize_product_id_string():
    oid = ObjectId()

    product = {"_id": oid, "name": "suco de laranja"}
    serialized_product = serialize_product(product)
    expected = {
        "id": str(oid),
        "name": "suco de laranja",
        "description": None,
        "category": None,
        "price": None,
        "available": True,
        "ingredients": [],
    }
    assert serialized_product == expected
