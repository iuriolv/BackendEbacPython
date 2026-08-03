from fastapi.testclient import TestClient
from main import app, Base, LivroDB
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL_TEST = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = mocker.patch('main.redis_client', autospec=True)
    mock_redis_client.get.return_value = None

@pytest.fixture(scope="function")
def db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_get_livros(db, mocker):
    response = client.get('/livros', auth=('admin', 'admin'))
    assert response.status_code == 200

    data = response.json()

    assert len(data['Livros']) == 9
    assert data['Livros'][0]['nome_livro'] == 'Harry Potter e a Pedra Filosofal'
    assert data['Livros'][0]['autor'] == 'J. K. Rowling'
    assert data['Livros'][0]['ano'] == 1997