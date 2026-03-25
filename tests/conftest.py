"""Pytest configuration and shared fixtures for API tests."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """Create a FastAPI TestClient for testing endpoints."""
    return TestClient(app)
