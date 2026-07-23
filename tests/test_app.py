import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test that GET /activities returns all activities"""
    # Arrange - nothing to arrange, we're just fetching
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "Soccer Club" in data
    assert "Basketball Team" in data
    assert "Chess Club" in data

def test_signup_for_activity_success():
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Soccer Club"
    email = "test@example.com"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert email in data["message"]

def test_signup_for_activity_not_found():
    """Test signup for non-existent activity returns 404"""
    # Arrange
    activity_name = "NonExistentActivity"
    email = "test@example.com"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "not found" in data["detail"].lower()

def test_signup_duplicate_email():
    """Test that signing up with duplicate email returns 400"""
    # Arrange
    activity_name = "Basketball Team"
    email = "duplicate@example.com"
    
    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act - try to signup again with same email
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()