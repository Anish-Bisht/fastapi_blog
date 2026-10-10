import pytest
from httpx import AsyncClient

from tests.conftest import auth_headers, create_test_user, login_user


@pytest.mark.anyio
async def test_forgot_password_returns_202_for_known_user(client: AsyncClient):
    await create_test_user(client, email="reset-user@example.com")

    response = await client.post(
        "/api/users/forget-password",
        json={"email": "reset-user@example.com"},
    )

    assert response.status_code == 202
    assert response.json()["message"] == "If the email exists, a password reset link has been sent."


@pytest.mark.anyio
async def test_health_check_returns_healthy(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
