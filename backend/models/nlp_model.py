"""NLP model implementation."""

from typing import Any, Dict, List

from backend.utils.logger import get_logger

logger = get_logger("NLPModel")


class PhishingNLPModel:
    """A simulated Distilled BERT for Phishing Text Detection."""

    def __init__(self) -> None:
        """Initialize the NLP model."""
        logger.info("Loading NLP Model (Distilled BERT)...")
        self.keywords: List[str] = [
            "urgent",
            "verify",
            "account",
            "suspended",
            "password",
            "click",
            "bank",
            "update",
        ]
        logger.info("NLP Model Loaded Successfully.")

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for malicious intent.

        Args:
            text (str): Input text content.

        Returns:
            Dict[str, Any]: Prediction results including score and intent.
        """
        if not text:
            return {
                "nlp_score": 0.0,
                "intent": "neutral",
                "urgency_detected": False,
                "extracted_entities": [],
            }

        text_lower = text.lower()

        # Heuristic: Keyword density
        hit_count = sum(1 for word in self.keywords if word in text_lower)

        # Base score
        maliciousness = 0.1
        if hit_count > 0:
            maliciousness += hit_count * 0.15

        # Check for length (phishing often short & urgent)
        if len(text) < 200 and hit_count > 1:
            maliciousness += 0.2

        maliciousness = min(max(maliciousness, 0.0), 1.0)

        intent = "neutral"
        if maliciousness > 0.7:
            intent = "credential_harvesting"
        elif maliciousness > 0.4:
            intent = "spam"

        return {
            "nlp_score": round(maliciousness * 100, 2),
            "intent": intent,
            "urgency_detected": "urgent" in text_lower,
            "extracted_entities": [w for w in self.keywords if w in text_lower],
        }
