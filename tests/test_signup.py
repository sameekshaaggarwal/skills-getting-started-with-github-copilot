"""Tests for signup and unregister endpoints."""

import pytest


def test_signup_success(client):
    """Test successfully signing up for an activity."""
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_signup_verification(client):
    """Test that signup actually adds the student to participants."""
    email = "verify@mergington.edu"
    activity = "Programming Class"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity]["participants"].copy()
    
    # Sign up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Verify student was added
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity]["participants"]
    
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_nonexistent_activity(client):
    """Test signup fails for non-existent activity."""
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate(client):
    """Test that a student cannot sign up twice for the same activity."""
    email = "duplicate@mergington.edu"
    activity = "Gym Class"
    
    # First signup
    response1 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup (should fail)
    response2 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_unregister_success(client):
    """Test successfully unregistering from an activity."""
    email = "unregister@mergington.edu"
    activity = "Chess Club"
    
    # First sign up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Then unregister
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_verification(client):
    """Test that unregister actually removes the student from participants."""
    email = "verify_unregister@mergington.edu"
    activity = "Programming Class"
    
    # Sign up
    client.post(f"/activities/{activity}/signup", params={"email": email})
    
    # Verify student is in list
    response_before = client.get("/activities")
    assert email in response_before.json()[activity]["participants"]
    
    # Unregister
    client.delete(f"/activities/{activity}/signup", params={"email": email})
    
    # Verify student is removed
    response_after = client.get("/activities")
    assert email not in response_after.json()[activity]["participants"]


def test_unregister_nonexistent_activity(client):
    """Test unregister fails for non-existent activity."""
    email = "student@mergington.edu"
    activity = "Nonexistent Club"
    
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_unregister_not_signed_up(client):
    """Test unregister fails when student is not signed up."""
    email = "notsignedup@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()
