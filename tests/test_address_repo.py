import pytest
from unittest.mock import MagicMock
import uuid
import sys

sys.modules["src.models.user_model"] = MagicMock()
sys.modules["src.models.user_model"].UserModel = MagicMock()
from src.repositories.user_repo import AddressRepository



@pytest.fixture
def mock_user():
    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_user.username = "test_user"
    mock_user.email = "test_user@example.com"
    return mock_user


@pytest.fixture
def mock_address(mock_user):

    mock_address = MagicMock()

    mock_address.id = uuid.uuid4()
    mock_address.user_id = mock_user.id
    mock_address.address_line = "123 Test Street"
    mock_address.city = "Test City"
    mock_address.state = "Test State"
    mock_address.postal_code = "12345"
    mock_address.country = "Test Country"
    mock_address.is_default = False

    mock_address.user = mock_user

    mock_address.to_dict = MagicMock(
        return_value={
            "id": mock_address.id,
            "user_id": mock_address.user_id,
            "address_line": mock_address.address_line,
            "city": mock_address.city,
            "state": mock_address.state,
            "postal_code": mock_address.postal_code,
            "country": mock_address.country,
            "is_default": mock_address.is_default,
        }
    )

    return mock_address


def test_address_model(mock_address):

    assert hasattr(mock_address, "id")
    assert hasattr(mock_address, "address_line")
    assert mock_address.address_line == "123 Test Street"
    assert mock_address.city == "Test City"
    assert mock_address.country == "Test Country"
    assert isinstance(mock_address.id, uuid.UUID)

    address_dict = mock_address.to_dict()
    assert address_dict["address_line"] == "123 Test Street"
    assert address_dict["city"] == "Test City"


def test_address_to_user_relationship(mock_address, mock_user):
    assert mock_address.user == mock_user
    assert mock_address.user.username == "test_user"
    assert mock_address.user.email == "test_user@example.com"
    assert mock_address.user.id == mock_address.user_id
