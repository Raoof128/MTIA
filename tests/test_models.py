"""Unit tests for AI models and engines."""

from PIL import Image

from backend.engines.exif_engine import ForensicsEngine
from backend.models.fusion_model import MultimodalFusionEngine
from backend.models.nlp_model import PhishingNLPModel
from backend.models.vision_model import PhishingVisionModel


def test_nlp_model():
    """Test NLP model prediction."""
    model = PhishingNLPModel()
    res = model.predict("Urgent update required for your account")
    assert res["urgency_detected"] is True
    assert res["nlp_score"] > 0


def test_vision_model():
    """Test Vision model prediction."""
    model = PhishingVisionModel()
    # Create a dummy red image
    img = Image.new("RGB", (100, 100), color="red")
    res = model.predict(img)
    assert "vision_score" in res
    assert isinstance(res["vision_score"], float)


def test_forensics_engine():
    """Test Forensics engine header analysis."""
    engine = ForensicsEngine()
    headers = {"SPF": "fail", "DKIM": "pass"}
    res = engine.analyze_headers(headers)
    assert res["forensic_score"] == 30
    assert "SPF_FAIL" in res["anomalies"]


def test_fusion_engine():
    """Test Fusion engine score calculation."""
    engine = MultimodalFusionEngine()
    vision = {"vision_score": 90}
    nlp = {"nlp_score": 80}
    forensics = {"forensic_score": 50}
    enrichment = {"reputation_score": 20}  # Risk = 100 - 20 = 80

    res = engine.fuse(vision, nlp, forensics, enrichment)
    # 90*0.3 + 80*0.3 + 50*0.2 + 80*0.2
    # 27 + 24 + 10 + 16 = 77.0
    assert res["final_threat_score"] == 77.0
    assert res["threat_level"] == "HIGH"


def test_enrichment_engine():
    """Test Enrichment engine domain analysis."""
    from backend.engines.enrichment import ThreatEnrichmentEngine

    engine = ThreatEnrichmentEngine()

    # Test bad domain
    res = engine.enrich_domain("secure-login-update.com")
    assert res["reputation_score"] == 0
    assert "T1566: Phishing" in res["mitre_tactics"]

    # Test extraction
    text = "Please visit http://example.com/login"
    domain = engine.extract_domain_from_text(text)
    assert domain == "example.com"
