from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

client = TestClient(app)

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_blog(test_data):
    test_blog = {"title": "string", "description": "string"}
    response = client.post(
        "/blogs", json=test_blog
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Blog created successfully"


def test_get_blog(test_data):
    response = client.get("/blogs/")
    assert response.status_code == 200
    assert len(response.json()) > 0


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)