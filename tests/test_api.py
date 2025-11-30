"""Integration tests for the FastAPI backend."""

from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "models": "loaded"}


def test_analyze_text_only():
    """Test analysis with text input only."""
    response = client.post(
        "/api/analyze",
        data={
            "text": "Urgent! Update your bank account now.",
            "spf": "pass",
            "dkim": "pass",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "fusion" in data
    assert "nlp" in data
    assert data["nlp"]["urgency_detected"] is True
    assert data["fusion"]["threat_level"] != "LOW"


def test_analyze_clean_text():
    """Test analysis with benign text."""
    response = client.post(
        "/api/analyze",
        data={"text": "Hello, how are you today?", "spf": "pass", "dkim": "pass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nlp"]["intent"] == "neutral"


def test_analyze_bad_headers():
    """Test analysis with spoofed headers."""
    response = client.post(
        "/api/analyze",
        data={"text": "Hello", "spf": "fail", "dkim": "fail"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["forensics"]["forensic_score"] > 0
    assert "SPF_FAIL" in data["forensics"]["anomalies"]
