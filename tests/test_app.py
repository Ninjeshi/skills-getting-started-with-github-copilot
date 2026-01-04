import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "participants" in data["Basketball"]

def test_signup_for_activity_success():
    email = "testuser@mergington.edu"
    activity = "Basketball"
    # Remove if already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json().get("message", "")
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_duplicate():
    email = "testuser2@mergington.edu"
    activity = "Tennis Club"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")

# Unregister endpoint test (if implemented)
def test_unregister_participant():
    email = "unregistertest@mergington.edu"
    activity = "Art Studio"
    # Ensure user is signed up
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code in (200, 404)  # 404 if already removed
    # Should not be in participants
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
