from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_create_blog():
    response = client.post("/blogs/", json={"title": "Test Blog", "content": "Test Content"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Blog"