"""Fusion engine implementation."""

from typing import Any, Dict

from backend.utils.logger import get_logger

logger = get_logger("FusionEngine")


class MultimodalFusionEngine:
    """Engine to combine scores from multiple models."""

    def __init__(self) -> None:
        """Initialize the fusion engine."""
        logger.info("Initializing Multimodal Fusion Engine...")

    def fuse(
        self,
        vision_result: Dict[str, Any],
        nlp_result: Dict[str, Any],
        forensic_result: Dict[str, Any],
        enrichment_result: Dict[str, Any] = {},
    ) -> Dict[str, Any]:
        """
        Combine scores using a weighted average.

        Args:
            vision_result (Dict[str, Any]): Result from vision model.
            nlp_result (Dict[str, Any]): Result from NLP model.
            forensic_result (Dict[str, Any]): Result from forensics engine.
            enrichment_result (Dict[str, Any]): Result from threat enrichment.

        Returns:
            Dict[str, Any]: Final fused threat intelligence.
        """
        v_score = float(vision_result.get("vision_score", 0))
        n_score = float(nlp_result.get("nlp_score", 0))
        f_score = float(forensic_result.get("forensic_score", 0))

        # Enrichment impact (Reputation is 0-100 where 100 is GOOD)
        e_score = 0.0
        if enrichment_result:
            reputation = float(enrichment_result.get("reputation_score", 50))
            e_score = max(0.0, 100.0 - reputation)  # 100 reputation = 0 risk

        # Weights (Sum = 1.0)
        w_v = 0.3
        w_n = 0.3
        w_f = 0.2
        w_e = 0.2

        final_score = (
            (v_score * w_v) + (n_score * w_n) + (f_score * w_f) + (e_score * w_e)
        )

        # Boost score if MITRE tactics are present
        if enrichment_result.get("mitre_tactics"):
            final_score += 15.0

        final_score = min(final_score, 100.0)

        threat_level = "LOW"
        if final_score > 80:
            threat_level = "CRITICAL"
        elif final_score > 50:
            threat_level = "HIGH"
        elif final_score > 20:
            threat_level = "MODERATE"

        return {
            "final_threat_score": round(final_score, 2),
            "threat_level": threat_level,
            "components": {
                "vision": v_score,
                "nlp": n_score,
                "forensics": f_score,
                "enrichment": e_score,
            },
            "recommendation": self._get_recommendation(threat_level),
        }

    def _get_recommendation(self, level: str) -> str:
        if level == "CRITICAL":
            return "BLOCK IMMEDIATELY. Isolate endpoint."
        elif level == "HIGH":
            return "Flag for manual review. Quarantine email."
        elif level == "MODERATE":
            return "Tag as suspicious. Warn user."
        return "No action needed."
