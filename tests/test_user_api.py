import pytest
from sqlalchemy import text
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_user_success(client):
    """Проверка успешного создания пользователя."""
    response = await client.post(
        "/users",
        json={"name": "John", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John"
    assert data["surname"] == "Doe"
    assert "password" in data
    assert "id" in data
    assert UUID(data["id"])

@pytest.mark.asyncio
async def test_create_user_missing_field(client):
    """Проверка ошибки при отсутствии обязательного поля."""
    response = await client.post(
        "/users",
        json={"name": "John", "password": "Secret1!"}
    )
    logger.info(f"Response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 400
    data = response.json()
    assert "surname" in str(data["extra"][0]["key"])

@pytest.mark.asyncio
async def test_create_user_empty_field(client):
    """Проверка ошибки при пустом значении поля."""
    response = await client.post(
        "/users",
        json={"name": "", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 400
    data = response.json()
    assert "name" in str(data["extra"][0]["key"])

@pytest.mark.asyncio
async def test_get_users_empty(client):
    """Проверка получения пустого списка пользователей."""
    response = await client.get("/users")
    logger.info(f"Response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_users_after_create(client):
    """Проверка получения списка пользователей после создания."""
    create_response = await client.post(
        "/users",
        json={"name": "John", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Create response status: {create_response.status_code}, body: {create_response.text}")
    assert create_response.status_code == 201
    response = await client.get("/users")
    logger.info(f"Get response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1, f"Expected 1 user, got {len(data)}: {data}"
    assert data[0]["name"] == "John"
    assert data[0]["surname"] == "Doe"
    assert "id" in data[0]

@pytest.mark.asyncio
async def test_get_user_by_id(client):
    """Проверка получения пользователя по ID."""
    create_response = await client.post(
        "/users",
        json={"name": "John", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Create response status: {create_response.status_code}, body: {create_response.text}")
    assert create_response.status_code == 201
    data = create_response.json()
    user_id = data["id"]
    response = await client.get(f"/users/{user_id}")
    logger.info(f"Get response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "John"

@pytest.mark.asyncio
async def test_get_user_by_id_not_found(client):
    """Проверка ошибки при попытке получить несуществующего пользователя."""
    response = await client.get("/users/123e4567-e89b-12d3-a456-426614174000")
    logger.info(f"Response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_update_user(client):
    """Проверка обновления пользователя."""
    create_response = await client.post(
        "/users",
        json={"name": "John", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Create response status: {create_response.status_code}, body: {create_response.text}")
    assert create_response.status_code == 201
    data = create_response.json()
    user_id = data["id"]
    response = await client.put(
        f"/users/{user_id}",
        json={"name": "Jane", "surname": "Smith", "password": "Secret2!"}
    )
    logger.info(f"Update response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane"
    assert data["surname"] == "Smith"

@pytest.mark.asyncio
async def test_delete_user(client):
    """Проверка удаления пользователя."""
    create_response = await client.post(
        "/users",
        json={"name": "John", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Create response status: {create_response.status_code}, body: {create_response.text}")
    assert create_response.status_code == 201
    data = create_response.json()
    user_id = data["id"]
    response = await client.delete(f"/users/{user_id}")
    logger.info(f"Delete response status: {response.status_code}, body: {response.text}")
    assert response.status_code == 204
    get_response = await client.get(f"/users/{user_id}")
    logger.info(f"Get response status: {get_response.status_code}, body: {get_response.text}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_database_persistence(client):
    """Проверка, что данные сохраняются в базе данных."""
    create_response = await client.post(
        "/users",
        json={"name": "John", "surname": "Doe", "password": "Secret1!"}
    )
    logger.info(f"Create response status: {create_response.status_code}, body: {create_response.text}")
    assert create_response.status_code == 201
    data = create_response.json()
    user_id = data["id"]
    engine = client.app.state.get("db_engine")
    if engine is None:
        logger.error("Engine not found in app.state")
        pytest.fail("Engine not found in app.state")
    async with engine.connect() as conn:
        result = await conn.execute(text('SELECT * FROM "user" WHERE id = :user_id'), {"user_id": user_id})
        user = result.first()
        if user is None:
            logger.error(f"No user found with id {user_id}")
            pytest.fail(f"No user found with id {user_id}")
        assert user.name == "John"
        assert user.surname == "Doe"