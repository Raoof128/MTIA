# Multimodal Threat Intelligence AI

[![CI](https://github.com/yourusername/multimodal-threat-intel/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/multimodal-threat-intel/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-grade, autonomous threat intelligence system that fuses **Computer Vision**, **Natural Language Processing (NLP)**, **Digital Forensics**, and **Threat Enrichment** to detect phishing, malware, and social engineering threats in real-time.

---

## 🏗 Architecture

The system uses a **Multimodal Fusion Engine** to combine signals from four distinct pipelines into a single, actionable threat score.

```mermaid
graph TD
    User[User Input] --> API[FastAPI Backend]
    API --> Vision[Vision Pipeline<br/>(CNN/ViT)]
    API --> NLP[NLP Pipeline<br/>(Distilled BERT)]
    API --> Forensics[Forensics Engine<br/>(EXIF/Headers)]
    API --> Enrichment[Enrichment Engine<br/>(WHOIS/Reputation)]
    
    Vision -->|Vision Score| Fusion[Fusion Engine]
    NLP -->|Maliciousness Score| Fusion
    Forensics -->|Risk Score| Fusion
    Enrichment -->|Reputation Score| Fusion
    
    Fusion -->|Final Threat Score| Dashboard[React/JS Dashboard]
```

### Core Components

1.  **Vision Pipeline (`backend/models/vision_model.py`)**
    *   Analyzes screenshots for brand impersonation and visual anomalies.
    *   Simulated lightweight CNN architecture.
    *   Detects suspicious color patterns and UI inconsistencies.

2.  **NLP Pipeline (`backend/models/nlp_model.py`)**
    *   Analyzes email bodies and text content.
    *   Uses heuristic keyword density and intent classification.
    *   Detects urgency, financial pressure, and credential harvesting attempts.

3.  **Forensics Engine (`backend/engines/exif_engine.py`)**
    *   Parses image EXIF metadata for device fingerprinting.
    *   Analyzes email headers (SPF, DKIM, DMARC) for spoofing detection.

4.  **Enrichment Engine (`backend/engines/enrichment.py`)**
    *   Extracts domains from text.
    *   Simulates WHOIS lookups (domain age).
    *   Simulates Reputation checks and MITRE ATT&CK mapping.

5.  **Fusion Engine (`backend/models/fusion_model.py`)**
    *   Aggregates scores using a weighted attention mechanism.
    *   Weights: Vision (30%), NLP (30%), Forensics (20%), Enrichment (20%).
    *   Outputs a final `CRITICAL`, `HIGH`, `MODERATE`, or `LOW` threat level.

---

## 🚀 Getting Started

### Prerequisites

*   Python 3.9 or higher
*   `pip` package manager
*   (Optional) Docker / VS Code Dev Containers

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/multimodal-threat-intel.git
    cd multimodal-threat-intel
    ```

2.  **Install dependencies**:
    ```bash
    make install
    # OR
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the Backend API**:
    ```bash
    make run
    # OR
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
    ```

2.  **Access the Dashboard**:
    Open your browser and navigate to:
    [http://localhost:8000](http://localhost:8000)

---

## 🧪 Testing

This project includes a comprehensive test suite using `pytest`.

To run the tests:
```bash
make test
```

To run linting and formatting checks:
```bash
make lint
make format
```

---

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:
[http://localhost:8000/docs](http://localhost:8000/docs)

### Key Endpoints

*   `POST /api/analyze`: Main analysis endpoint. Accepts text and optional image file.
*   `GET /health`: System health check.

---

## 🔒 Security & Privacy

*   **Local Execution**: All processing happens locally on your machine. No data is sent to external cloud services.
*   **Synthetic Data**: The models are trained/simulated on synthetic data for educational safety.
*   **Input Validation**: All inputs are strictly validated using Pydantic schemas.

**Disclaimer**: This tool is for **EDUCATIONAL PURPOSES ONLY**. Do not use it to analyze real-world sensitive PII or rely on it for critical security defense without further hardening.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
