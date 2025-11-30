"""Threat enrichment engine implementation."""

import datetime
import random
from typing import Any, Dict

from backend.utils.logger import get_logger

logger = get_logger("EnrichmentEngine")


class ThreatEnrichmentEngine:
    """
    Simulates external Threat Intelligence lookups (WHOIS, Reputation, SSL).

    In a real system, this would query VirusTotal, AlienVault, or DomainTools.
    """

    def __init__(self) -> None:
        """Initialize the enrichment engine."""
        logger.info("Initializing Threat Enrichment Engine (Simulated)...")
        self.suspicious_tlds = [".xyz", ".top", ".gq", ".tk", ".cn"]
        self.known_bad_domains = [
            "secure-login-update.com",
            "verify-account-now.net",
        ]

    def enrich_domain(self, domain: str) -> Dict[str, Any]:
        """
        Perform simulated WHOIS and Reputation lookups.

        Args:
            domain (str): The domain to analyze.

        Returns:
            Dict[str, Any]: Enrichment data including domain age,
                registrar, and reputation.
        """
        if not domain:
            return {}

        logger.info(f"Enriching domain: {domain}")

        # 1. Simulated WHOIS (Domain Age)
        # Randomly assign age. New domains (< 30 days) are riskier.
        # Deterministic seed based on domain name for consistent demo results
        random.seed(domain)
        days_active = random.randint(1, 3650)

        # If domain looks "bad" (heuristic), make it young
        if any(tld in domain for tld in self.suspicious_tlds) or "login" in domain:
            days_active = random.randint(1, 15)

        creation_date = datetime.date.today() - datetime.timedelta(days=days_active)

        # 2. Simulated SSL Info
        ssl_issuer = "Let's Encrypt" if days_active < 90 else "DigiCert Inc"

        # 3. Simulated Reputation Score (0-100, where 100 is clean)
        reputation = random.randint(0, 100)
        if days_active < 30:
            reputation = max(0, reputation - 40)
        if domain in self.known_bad_domains:
            reputation = 0

        # 4. MITRE ATT&CK Mapping (Simulated)
        mitre_tactics = []
        if reputation < 50:
            mitre_tactics.append("T1566: Phishing")
            mitre_tactics.append("T1583: Acquire Infrastructure")

        return {
            "domain_age_days": days_active,
            "creation_date": str(creation_date),
            "registrar": (
                "GoDaddy.com, LLC" if days_active > 365 else "NameCheap, Inc."
            ),
            "ssl_issuer": ssl_issuer,
            "reputation_score": reputation,
            "mitre_tactics": mitre_tactics,
            "risk_level": "HIGH" if reputation < 40 else "LOW",
        }

    def extract_domain_from_text(self, text: str) -> str:
        """Extract the first domain-like string from text using robust parsing."""
        from urllib.parse import urlparse

        words = text.split()
        for word in words:
            # Check if it looks like a URL
            if "http" in word or "www" in word:
                try:
                    # Add http if missing for parsing
                    if not word.startswith("http"):
                        parse_url = "http://" + word
                    else:
                        parse_url = word

                    parsed = urlparse(parse_url)
                    if parsed.netloc:
                        return parsed.netloc
                except Exception:
                    continue

            # Fallback for simple domains like "google.com"
            if "." in word and "@" not in word:
                clean = word.strip(".,;:()[]")
                if len(clean) > 4:
                    return clean
        return ""
