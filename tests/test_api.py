from fastapi.testclient import TestClient

from main import INSTANCE_ID, app

client = TestClient(app)


def test_root_endpoint():
    """Test 1: Root endpoint is available and identifies the instance."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["instance_id"] == INSTANCE_ID
    assert "Load-balanced application is running" in data["message"]


def test_health_check():
    """Test 2: Health endpoint reports a healthy instance."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["instance_id"] == INSTANCE_ID
    assert "timestamp" in data


def test_instance_endpoint():
    """Test 3: Instance endpoint exposes the instance identifier and hostname."""
    response = client.get("/instance")
    assert response.status_code == 200
    data = response.json()
    assert data["instance_id"] == INSTANCE_ID
    assert data["hostname"]
    assert data["timestamp"]


def test_multiple_requests_are_served():
    """Test 4: Service can handle a burst of requests without errors."""
    responses = [client.get("/instance") for _ in range(20)]
    assert all(response.status_code == 200 for response in responses)
    assert all(response.json()["instance_id"] == INSTANCE_ID for response in responses)
