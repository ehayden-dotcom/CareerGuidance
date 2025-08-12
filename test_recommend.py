"""Tests for the recommendation endpoint."""
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.models import seed_db_if_needed


def test_recommend_returns_three_recommendations() -> None:
    seed_db_if_needed()
    client = TestClient(app)
    profile = {
        "name": "Test Student",
        "yearLevel": 10,
        "interests": ["IT", "STEM"],
        "strengths": ["Problem-Solving", "Technical Skills"],
        "academicPerformance": "High",
    }
    response = client.post("/api/recommend", json=profile)
    assert response.status_code == 200
    recs = response.json()
    assert isinstance(recs, list)
    assert len(recs) == 3
    for rec in recs:
        # Confidence should be a float between 0 and 1 inclusive
        assert 0.0 <= rec["confidence"] <= 1.0
        assert rec["why"]