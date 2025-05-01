import pytest
from unittest.mock import (
    MagicMock,
    patch,
)
import sys
from datetime import datetime
import uuid

# Prevent the real UserModel from being loaded
sys.modules["src.models.user_model"] = MagicMock()
sys.modules["src.models.user_model"].UserModel = MagicMock()

# Now import the repository
from src.repositories.user_repo import (
    UserRepository,
)


@pytest.fixture
def mock_users():
    users_list = []

    for i in range(3):

        mock_user = MagicMock()

        user_id = uuid.uuid4()
        mock_user.id = user_id
        mock_user.username = f"user{i+1}"
        mock_user.email = f"user{i+1}@example.com"
        mock_user.fullname = f"User {i+1}"
        mock_user.phone = f"123456789{i}"
        mock_user.birth_date = datetime.now()
        mock_user.created_at = datetime.now()
        mock_user.updated_at = datetime.now()
        mock_user.is_activate = i != 2
        mock_user.is_locked = i == 2
        mock_user.role_id = 1
        mock_user.hash_password = f"hashed_password_{i+1}"

        mock_user.role = MagicMock()
        mock_user.token = MagicMock()
        mock_user.address = MagicMock()

        mock_user.to_dict = MagicMock(
            return_value={
                "id": user_id,
                "username": f"user{i+1}",
                "email": f"user{i+1}@example.com",
                "fullname": f"User {i+1}",
                "phone": f"123456789{i}",
                "birth_date": mock_user.birth_date,
                "created_at": mock_user.created_at,
                "update_at": mock_user.updated_at,
                "is_activate": mock_user.is_activate,
                "is_locked": mock_user.is_locked,
            }
        )

        users_list.append(mock_user)

    return users_list


@pytest.fixture
def patched_user_model():
    mock_user_model = MagicMock()
    mock_user_model.__tablename__ = "users"
    return mock_user_model


@pytest.fixture
def user_repository(patched_user_model):
    UserRepository.model = patched_user_model
    return UserRepository()


def test_user_repository_model(
    mock_users,
    user_repository,
    patched_user_model,
):

    assert isinstance(UserRepository.model, MagicMock)

    sample_user = mock_users[0]

    assert hasattr(sample_user, "id")
    assert hasattr(sample_user, "username")
    assert hasattr(sample_user, "email")
    assert hasattr(sample_user, "fullname")
    assert hasattr(sample_user, "birth_date")
    assert hasattr(sample_user, "created_at")
    assert hasattr(sample_user, "updated_at")
    assert hasattr(sample_user, "is_activate")
    assert hasattr(sample_user, "is_locked")
    assert hasattr(sample_user, "role_id")
    assert hasattr(sample_user, "hash_password")

    assert sample_user.username == "user1"
    assert sample_user.email == "user1@example.com"
    assert sample_user.fullname == "User 1"

    assert isinstance(sample_user.birth_date, datetime)
    assert isinstance(sample_user.created_at, datetime)
    assert isinstance(sample_user.updated_at, datetime)

    assert sample_user.is_activate is True
    assert sample_user.is_locked is False

    assert sample_user.role_id == 1

    assert sample_user.hash_password == "hashed_password_1"


# по приколу проганяємо 3-х юзерів
def test_all_mock_users(mock_users):

    assert len(mock_users) == 3

    for i, user in enumerate(mock_users):
        assert user.username == f"user{i+1}"
        assert user.email == f"user{i+1}@example.com"
        assert user.fullname == f"User {i+1}"
        assert user.phone == f"123456789{i}"
        assert isinstance(user.birth_date, datetime)
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)
        assert user.role_id == 1
        assert user.hash_password == f"hashed_password_{i+1}"

    assert mock_users[2].is_activate is False
    assert mock_users[2].is_locked is True
    assert mock_users[0].is_activate is True
    assert mock_users[0].is_locked is False
    assert mock_users[1].is_activate is True
    assert mock_users[1].is_locked is False
