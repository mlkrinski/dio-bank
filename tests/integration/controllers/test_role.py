from http import HTTPStatus
from src.app import db, Role


def test_create_role(client):
    # Given
    payload = {"name": "admin"}

    # When
    response = client.post("/roles/", json=payload)

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Role created!"}

    # E valida se realmente salvou no banco
    role = db.session.execute(db.select(Role).where(Role.name == "admin")).scalar()
    assert role is not None
    assert role.name == "admin"
