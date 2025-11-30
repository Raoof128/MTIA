"""Forensics engine implementation."""

from typing import Any, Dict, List

from PIL import ExifTags, Image

from backend.utils.logger import get_logger

logger = get_logger("ForensicsEngine")


class ForensicsEngine:
    """Engine to extract EXIF data and analyze headers."""

    def __init__(self) -> None:
        """Initialize the forensics engine."""
        pass

    def extract_exif(self, image: Image.Image) -> Dict[str, str]:
        """
        Extract EXIF data from an image.

        Args:
            image (Image.Image): Input PIL image.

        Returns:
            Dict[str, str]: Extracted EXIF tags and values.
        """
        exif_data: Dict[str, str] = {}
        try:
            img_exif = image.getexif()
            if img_exif:
                for tag_id, value in img_exif.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    exif_data[str(tag)] = str(value)
        except Exception as e:
            logger.error(f"Error extracting EXIF: {e}")

        return exif_data

    def analyze_headers(self, headers: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze email headers for spoofing (SPF/DKIM/DMARC).

        Args:
            headers (Dict[str, str]): Dictionary of email headers.

        Returns:
            Dict[str, Any]: Analysis result including score and anomalies.
        """
        score = 0
        anomalies: List[str] = []

        # Mock checks
        if headers.get("SPF") == "fail":
            score += 30
            anomalies.append("SPF_FAIL")
        if headers.get("DKIM") == "fail":
            score += 30
            anomalies.append("DKIM_FAIL")

        return {"forensic_score": score, "anomalies": anomalies}
