"""Main API entrypoint."""

import io
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel

from backend.engines.enrichment import ThreatEnrichmentEngine
from backend.engines.exif_engine import ForensicsEngine
from backend.models.fusion_model import MultimodalFusionEngine
from backend.models.nlp_model import PhishingNLPModel
from backend.models.vision_model import PhishingVisionModel
from backend.utils.logger import get_logger

logger = get_logger("MainAPI")

app = FastAPI(
    title="Multimodal Threat Intelligence AI",
    description=(
        "A production-grade, autonomous threat intelligence system "
        "that fuses Computer Vision, NLP, and Forensics."
    ),
    version="1.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Models
vision_model = PhishingVisionModel()
nlp_model = PhishingNLPModel()
fusion_engine = MultimodalFusionEngine()
forensics_engine = ForensicsEngine()
enrichment_engine = ThreatEnrichmentEngine()


# --- Pydantic Models ---
class VisionResult(BaseModel):
    """Result from vision analysis."""

    vision_score: float
    visual_class: str
    anomalies: List[str]
    heatmap_regions: str


class NLPResult(BaseModel):
    """Result from NLP analysis."""

    nlp_score: float
    intent: str
    urgency_detected: bool
    extracted_entities: List[str]


class ForensicsResult(BaseModel):
    """Result from forensics analysis."""

    forensic_score: int
    anomalies: List[str]
    exif_count: Optional[int] = 0


class EnrichmentResult(BaseModel):
    """Result from threat enrichment."""

    domain_age_days: Optional[int] = 0
    registrar: Optional[str] = "Unknown"
    reputation_score: Optional[int] = 50
    mitre_tactics: List[str] = []
    risk_level: Optional[str] = "UNKNOWN"


class FusionComponents(BaseModel):
    """Individual component scores."""

    vision: float
    nlp: float
    forensics: float
    enrichment: float


class FusionResult(BaseModel):
    """Final fused threat intelligence."""

    final_threat_score: float
    threat_level: str
    components: FusionComponents
    recommendation: str


class AnalysisResponse(BaseModel):
    """Complete analysis response."""

    fusion: FusionResult
    vision: VisionResult
    nlp: NLPResult
    forensics: ForensicsResult
    enrichment: EnrichmentResult


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_threat(
    text: str = Form(""),
    spf: str = Form("pass"),
    dkim: str = Form("pass"),
    file: Optional[UploadFile] = File(None),
) -> Dict[str, Any]:
    """
    Analyze threat using multimodal engines.

    Args:
        text (str): Input text.
        spf (str): SPF status.
        dkim (str): DKIM status.
        file (UploadFile): Optional image file.

    Returns:
        Dict[str, Any]: Analysis results.
    """
    logger.info("Received analysis request")

    # 1. Vision Analysis
    vision_result: Dict[str, Any] = {
        "vision_score": 0.0,
        "visual_class": "none",
        "anomalies": [],
        "heatmap_regions": "",
    }
    forensic_result: Dict[str, Any] = {"forensic_score": 0, "anomalies": []}

    if file:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents)).convert("RGB")
            vision_result = vision_model.predict(image)

            # Forensics (EXIF)
            exif_data = forensics_engine.extract_exif(image)
            # Add mock header analysis
            header_res = forensics_engine.analyze_headers({"SPF": spf, "DKIM": dkim})
            forensic_result = header_res
            forensic_result["exif_count"] = len(exif_data)
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            # Don't fail the whole request, just log and proceed with partial data
    else:
        # Even if no file, we still check headers
        forensic_result = forensics_engine.analyze_headers({"SPF": spf, "DKIM": dkim})
        forensic_result["exif_count"] = 0

    # 2. NLP Analysis
    nlp_result = nlp_model.predict(text)

    # 3. Threat Enrichment
    enrichment_result: Dict[str, Any] = {}
    extracted_domain = enrichment_engine.extract_domain_from_text(text)
    if extracted_domain:
        enrichment_result = enrichment_engine.enrich_domain(extracted_domain)
    else:
        # Default empty result
        enrichment_result = {
            "domain_age_days": 0,
            "registrar": "N/A",
            "reputation_score": 50,
            "mitre_tactics": [],
            "risk_level": "UNKNOWN",
        }

    # 4. Fusion
    fusion_result = fusion_engine.fuse(
        vision_result, nlp_result, forensic_result, enrichment_result
    )

    return {
        "fusion": fusion_result,
        "vision": vision_result,
        "nlp": nlp_result,
        "forensics": forensic_result,
        "enrichment": enrichment_result,
    }


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Check the health of the API."""
    return {"status": "healthy", "models": "loaded"}


# Serve Frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
