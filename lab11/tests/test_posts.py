from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_posts():
    response = client.get("/posts")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) >= 2

def test_create_post():
    new_post = {"id": 3, "title": "Third Post", "content": "This is the third post"}
    response = client.post("/posts", json=new_post)
    assert response.status_code == 200
    assert response.json() == new_post

def test_update_post():
    updated_post = {"id": 1, "title": "Updated First Post", "content": "Updated content"}
    response = client.put("/posts/1", json=updated_post)
    assert response.status_code == 200
    assert response.json() == updated_post

def test_delete_post():
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Post deleted"}
