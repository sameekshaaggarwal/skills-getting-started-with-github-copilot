"""Tests for the activities endpoint."""

import pytest


def test_get_all_activities(client):
    """Test retrieving all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify structure
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Verify expected activities exist
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_activities_structure(client):
    """Test that activity objects have the correct structure."""
    response = client.get("/activities")
    activities = response.json()
    
    # Check one activity's structure in detail
    chess_club = activities["Chess Club"]
    
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    assert isinstance(chess_club["description"], str)
    assert isinstance(chess_club["schedule"], str)
    assert isinstance(chess_club["max_participants"], int)
    assert isinstance(chess_club["participants"], list)


def test_activities_participants_are_emails(client):
    """Test that participants in activities are email addresses."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_details in activities.items():
        for email in activity_details["participants"]:
            assert isinstance(email, str)
            assert "@" in email
