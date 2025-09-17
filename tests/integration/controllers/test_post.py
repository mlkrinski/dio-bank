from http import HTTPStatus
from src.app import db, Post, User, Role


def test_create_post(client):
    # Given: um usuário autor do post
    role = Role(name="author")
    db.session.add(role)
    db.session.commit()

    user = User(username="john", password="123", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    payload = {"title": "Meu Primeiro Post", "body": "Conteúdo teste", "author_id": user.id}

    # When
    response = client.post("/posts/", json=payload)

    # Then
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "Post created!"}

    post = db.session.execute(db.select(Post).where(Post.title == "Meu Primeiro Post")).scalar()
    assert post is not None
    assert post.author_id == user.id


def test_list_posts(client):
    # Given
    posts = db.session.execute(db.select(Post)).scalars().all()

    # When
    response = client.get("/posts/")

    # Then
    assert response.status_code == HTTPStatus.OK
    data = response.json["posts"]
    assert isinstance(data, list)
    assert len(data) == len(posts)


def test_get_post_by_id(client):
    # Given
    post = Post(title="Teste", body="Conteúdo", author_id=1)
    db.session.add(post)
    db.session.commit()

    # When
    response = client.get(f"/posts/{post.id}")

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json["id"] == post.id
    assert response.json["title"] == "Teste"


def test_update_post(client):
    # Given
    post = Post(title="Antigo", body="Texto antigo", author_id=1)
    db.session.add(post)
    db.session.commit()

    payload = {"title": "Novo Título"}

    # When
    response = client.patch(f"/posts/{post.id}", json=payload)

    # Then
    assert response.status_code == HTTPStatus.OK
    assert response.json["title"] == "Novo Título"


def test_delete_post(client):
    # Given
    post = Post(title="Para deletar", body="Remover", author_id=1)
    db.session.add(post)
    db.session.commit()

    # When
    response = client.delete(f"/posts/{post.id}")

    # Then
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert db.session.get(Post, post.id) is None
