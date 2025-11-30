"""Vision model implementation."""

import random
from typing import Any, Dict, List

import numpy as np
from PIL import Image

from backend.utils.logger import get_logger

logger = get_logger("VisionModel")


class PhishingVisionModel:
    """
    A simulated Vision Transformer/CNN for Phishing Detection.

    In a real production environment, this would load weights from a .pt file.
    """

    def __init__(self) -> None:
        """Initialize the vision model."""
        logger.info("Loading Vision Model (Lightweight CNN)...")
        # Simulation of model loading
        self.classes: List[str] = ["benign", "phishing", "suspicious"]
        logger.info("Vision Model Loaded Successfully.")

    def preprocess(self, image: Image.Image) -> Image.Image:
        """
        Resize and normalize image.

        Args:
            image (Image.Image): Input PIL image.

        Returns:
            Image.Image: Preprocessed image.
        """
        return image.resize((224, 224))

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze image for visual threats.

        Args:
            image (Image.Image): Input PIL image.

        Returns:
            Dict[str, Any]: Prediction results including score and class.
        """
        try:
            # 1. Heuristic: Check for 'suspicious' colors
            # (e.g. excessive red/alert colors)
            # This is a MOCK implementation for the demo.
            img_array = np.array(image)
            if img_array.ndim == 2:  # Grayscale
                mean_red = np.mean(img_array)
            else:
                red_channel = img_array[:, :, 0]
                mean_red = np.mean(red_channel)

            # 2. Heuristic: Check for specific visual patterns
            # (simulated by random seed from image size)
            # This ensures deterministic output for the same image.
            seed = image.size[0] + image.size[1] + int(mean_red)
            random.seed(seed)

            phishing_score = random.uniform(0.1, 0.9)

            # Adjust score based on "red" content (simulating alert UI)
            if mean_red > 150:
                phishing_score += 0.1

            phishing_score = min(max(phishing_score, 0.0), 1.0)

            predicted_class = "benign"
            if phishing_score > 0.7:
                predicted_class = "phishing"
            elif phishing_score > 0.4:
                predicted_class = "suspicious"

            return {
                "vision_score": round(phishing_score * 100, 2),
                "visual_class": predicted_class,
                "anomalies": (["brand_impersonation"] if phishing_score > 0.8 else []),
                "heatmap_regions": "simulated_gradcam_overlay",
            }
        except Exception as e:
            logger.error(f"Error in vision prediction: {e}")
            return {
                "vision_score": 0.0,
                "visual_class": "error",
                "anomalies": [],
                "heatmap_regions": "",
            }
