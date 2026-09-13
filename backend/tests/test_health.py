from fastapi.testclient import TestClient
from app.main import app

def test_health() -> None:
    response = TestClient(app).get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_demo_login_and_ticket_access() -> None:
    with TestClient(app) as client:
        login = client.post("/api/v1/auth/login", json={"email": "admin@opsflow.dev", "password": "OpsFlow123!"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        response = client.get("/api/v1/tickets", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert len(response.json()) >= 3
