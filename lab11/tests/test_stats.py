from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "GET" in stats
    assert "POST" in stats
    assert "PUT" in stats
    assert "DELETE" in stats
