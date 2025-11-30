# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-01

### Added
- **Multimodal Fusion Engine**: Core logic to combine Vision, NLP, and Forensics scores.
- **Vision Pipeline**: Simulated CNN/ViT model for phishing screenshot analysis.
- **NLP Pipeline**: Simulated Distilled BERT model for malicious text detection.
- **Forensics Engine**: EXIF extraction and email header analysis (SPF/DKIM).
- **API**: FastAPI backend with `/api/analyze` endpoint.
- **Frontend**: Glassmorphism dashboard for real-time threat assessment.
- **Documentation**: Comprehensive README, Contributing guidelines, and Security policy.
- **CI/CD**: Basic Makefile and project configuration.

### Security
- Implemented input validation using Pydantic.
- Added safety warnings for educational use.
