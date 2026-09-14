from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

def test_health() -> None:
    response = TestClient(app).get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_demo_login_and_ticket_access() -> None:
    with TestClient(app) as client:
        login = client.post("/api/v1/auth/login", json={"email": "demo@opsflow.dev", "password": "Demo12345!"})
        assert login.status_code == 200
        token = login.json()["access_token"]
        response = client.get("/api/v1/tickets", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert len(response.json()) >= 3
        forbidden = client.post("/api/v1/customers", headers={"Authorization": f"Bearer {token}"}, json={"name": "Blocked Write", "email": "blocked@example.com", "phone": "+8801700000000"})
        assert forbidden.status_code == 403

def test_authenticated_operations_workflow() -> None:
    with TestClient(app) as client:
        login = client.post("/api/v1/auth/login", json={"email": "admin@opsflow.dev", "password": "OpsFlow123!"})
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        suffix = uuid4().hex[:8]
        customer = client.post("/api/v1/customers", headers=headers, json={"name": "Workflow Customer", "email": f"workflow-{suffix}@example.com", "phone": "+8801700000000"})
        assert customer.status_code == 201
        customer_id = customer.json()["id"]
        ticket = client.post("/api/v1/tickets", headers=headers, json={"customer_id": customer_id, "title": "Integration repair", "device": "Test device", "priority": "high", "estimated_cost": 250})
        assert ticket.status_code == 201
        updated = client.patch(f"/api/v1/tickets/{ticket.json()['id']}", headers=headers, json={"status": "in_progress"})
        assert updated.json()["status"] == "in_progress"
        item = client.post("/api/v1/inventory", headers=headers, json={"sku": f"TEST-{suffix}", "name": "Test component", "category": "Testing", "quantity": 2, "reorder_level": 1, "unit_cost": 20})
        assert item.status_code == 201
        stock = client.patch(f"/api/v1/inventory/{item.json()['id']}/stock?change=-1", headers=headers)
        assert stock.json()["quantity"] == 1
        invoice = client.post("/api/v1/invoices", headers=headers, json={"customer_id": customer_id, "ticket_id": ticket.json()["id"], "subtotal": 250, "paid": 50})
        assert invoice.status_code == 201
        payment = client.patch(f"/api/v1/invoices/{invoice.json()['id']}/payment", headers=headers, json={"amount": 200})
        assert payment.json()["status"] == "paid"
        stats = client.get("/api/v1/dashboard/stats", headers=headers)
        assert stats.status_code == 200
        assert stats.json()["customers"] >= 1
