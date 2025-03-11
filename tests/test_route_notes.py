from unittest.mock import MagicMock, patch, AsyncMock

import pytest

from scr.database.models import User
from scr.services.auth import auth_service


@pytest.fixture()
def token(client, user, session, monkeypatch):
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
    monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
    mock_send_email = MagicMock()
    monkeypatch.setattr("scr.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    return data["access_token"]


# def test_create_note(client, token, session, monkeypatch):
#     with patch.object(auth_service, 'cache') as r_mock:
#         r_mock.get.return_value = None
#         response = client.post(
#             "/api/notes",
#             json={"title": "title_test_note"},
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert response.status_code == 201, response.text
#         data = response.json()
#         assert data["title"] == "title_test_note"
#         assert "id" in data


