"""Tests for the root redirect endpoint."""

import pytest


def test_root_redirect(client):
    """Test that root endpoint redirects to static index.html."""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_follow(client):
    """Test that following the redirect returns the HTML page."""
    response = client.get("/", follow_redirects=True)
    
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
