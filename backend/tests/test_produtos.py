import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)  # cria tabelas
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # limpa tudo

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_criar_produto_sucesso(client):
    response = client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Notebook",
        "categoria_produto": "Eletronico"
    })

    assert response.status_code == 200


def test_criar_produto_duplicado(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Notebook",
        "categoria_produto": "Eletronico"
    })

    response = client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Notebook",
        "categoria_produto": "Eletronico"
    })

    assert response.status_code in [400, 409]


def test_criar_produto_invalido(client):
    response = client.post("/produtos/", json={
        "id_produto": "",
        "nome_produto": "",
        "categoria_produto": ""
    })

    assert response.status_code == 422


def test_listar_produtos_vazio(client):
    response = client.get("/produtos/")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_listar_produtos_com_dados(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Notebook",
        "categoria_produto": "Eletronico"
    })

    response = client.get("/produtos/")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_buscar_produto_existente(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Notebook",
        "categoria_produto": "Eletronico"
    })

    response = client.get("/produtos/p1")
    assert response.status_code == 200


def test_buscar_produto_inexistente(client):
    response = client.get("/produtos/nao_existe")
    assert response.status_code == 404


def test_buscar_por_nome_com_resultado(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Notebook",
        "categoria_produto": "Eletronico"
    })

    response = client.get("/produtos?nome=Note")
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


def test_buscar_por_nome_sem_resultado(client):
    response = client.get("/produtos?nome=xyz")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_atualizar_produto_sucesso(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Mouse",
        "categoria_produto": "Eletronico"
    })

    response = client.put("/produtos/p1", json={
        "nome_produto": "Mouse Gamer"
    })

    assert response.status_code == 200
    assert response.json()["nome_produto"] == "Mouse Gamer"


def test_atualizar_produto_inexistente(client):
    response = client.put("/produtos/nao_existe", json={
        "nome_produto": "Teste"
    })

    assert response.status_code == 404


def test_deletar_produto_sucesso(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Teclado",
        "categoria_produto": "Eletronico"
    })

    response = client.delete("/produtos/p1")
    assert response.status_code == 200


def test_deletar_produto_inexistente(client):
    response = client.delete("/produtos/nao_existe")
    assert response.status_code == 404

def test_media_sem_avaliacao(client):
    client.post("/produtos/", json={
        "id_produto": "p1",
        "nome_produto": "Cadeira",
        "categoria_produto": "Moveis"
    })

    response = client.get("/produtos/p1/media-avaliacoes")
    assert response.status_code == 200
    assert response.json()["media"] == 0.0


def test_media_produto_inexistente(client):
    response = client.get("/produtos/nao_existe/media-avaliacoes")
    assert response.status_code == 404
