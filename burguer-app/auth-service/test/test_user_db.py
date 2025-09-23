import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.user_model import serialize_user


@pytest.mark.usefixtures("test_db")
def test_insert_user(test_db):
    user = {
        "email": "teste@exemplo.com",
        "name": "Teste usuario",
    }

    result = test_db["users"].insert_one(user)
    find = test_db["users"].find_one({"_id": result.inserted_id})
    assert find["email"] == "teste@exemplo.com"
