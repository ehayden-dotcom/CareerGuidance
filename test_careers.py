"""Tests for the careers endpoints."""
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models import seed_db_if_needed


def test_list_careers_not_empty() -> None:
    # Ensure the database is seeded for the test
    seed_db_if_needed()
    client = TestClient(app)
    response = client.get("/api/careers")
    assert response.status_code == 200
    careers = response.json()
    assert isinstance(careers, list)
    assert len(careers) >= 1
    # Check that a few expected fields exist
    sample = careers[0]
    assert "careerId" in sample
    assert "name" in sample


def test_get_career_by_id() -> None:
    seed_db_if_needed()
    client = TestClient(app)
    # Choose a known career ID from the sample data
    career_id = "CR002"
    response = client.get(f"/api/careers/{career_id}")
    assert response.status_code == 200
    career = response.json()
    assert career["careerId"] == career_id