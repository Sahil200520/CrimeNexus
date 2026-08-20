# Crime Nexus: Crime Hotspot Mapping & Behavioural Analysis System (CT-DFIR-01) 🚔💻

[![Status: Proof-of-Concept](https://img.shields.io/badge/Status-Proof--of--Concept-amber.svg)](#disclaimer) [![Compliance: SC/ST Act](https://img.shields.io/badge/Ethics-SC%2FST%20Act%20Compliant-green.svg)](docs/governance/legal_opinion_memo.md) [![Data Privacy: DPDP Compliant](https://img.shields.io/badge/Privacy-DPDP%20Compliant-blue.svg)](docs/governance/data_privacy_policy.md)

> [!CAUTION]
> ### ⚠️ DISCLAIMER: PROOF-OF-CONCEPT — NOT FOR OPERATIONAL USE
> This software is a **research proof-of-concept (PoC)** developed under project **CT-DFIR-01** for analytical evaluation and decision support prototyping. It is **not validated for operational deployment**, real-time dispatch, or live law enforcement actions. All models (including recidivism scoring) are restricted to research evaluation mode.

---

## 📜 Table of Contents
1. [Overview & System Architecture](#overview--system-architecture)
2. [Governance & Ethical Principles](#governance--ethical-principles)
3. [Key Modules & Capabilities](#key-modules--capabilities)
    * [Crime Hotspot Mapping](#crime-hotspot-mapping)
    * [Legal Classification Tagging](#legal-classification-tagging)
    * [Patrol Route Allocation](#patrol-route-allocation)
    * [Accident-Prone Zone Overlay](#accident-prone-zone-overlay)
4. [Dual-Language Support (Tamil / English)](#dual-language-support)
5. [Installation & Setup](#installation--setup)
6. [Containerization (Docker)](#containerization-docker)
7. [Project Roadmap & Governance Docs](#project-governance-documents)

---

## Overview & System Architecture

**Crime Nexus (CT-DFIR-01)** provides law enforcement agencies with a modernized, data-driven analytical platform for crime pattern analysis, spatial-temporal hotspot mapping, legal section tagging, societal trend forecasting, and optimal patrol route generation.

The platform prioritizes strict ethical AI governance, legal compliance under statutory non-discrimination acts, explainable models, and dual-language usability (Tamil / English).

---

## Governance & Ethical Principles

This project operates under strict legal and ethical directives established in Phase 1:

- **No Protected Characteristics:** Complete excision of caste, religion, and protected demographic features from model inputs and analytics charts in accordance with the SC/ST (Prevention of Atrocities) Act and Article 15 of the Constitution of India. See [Legal Opinion Memo](docs/governance/legal_opinion_memo.md) and [Formal Decision Record](docs/governance/decision_record_caste_removal.md).
- **Data Privacy & PII Handling:** Mandatory anonymization, SHA-256 name hashing, contact masking, and spatial coordinate jittering ($\pm 500\text{m}$) for FIR records. See [Data Privacy & PII Policy](docs/governance/data_privacy_policy.md).
- **Recidivism Scope Restriction:** The recidivism prediction module is restricted to a **Research-Only** track (`RESEARCH_MODE_ENABLED=true`). See [Recidivism Scope Decision](docs/governance/recidivism_scope_decision.md).
- **Synthetic Data Governance:** Demonstration builds rely on realistically formatted synthetic FIR datasets to safeguard privacy. See [Data Source Decision](docs/governance/data_source_decision.md).

---

## Key Modules & Capabilities

- **Unified Hotspot Mapping:** Interactive spatial-temporal maps filtering by crime type, date ranges, season, and legal classification (IPC / NDPS / Arms Act).
- **Accident-Prone Zone Integration:** Toggleable overlay of accident hotspot data integrated alongside crime clusters.
- **Societal & Seasonal Trend Forecasting:** Time-series forecasting for proactive seasonal planning.
- **Dynamic Patrol Route Generation:** Automated patrol route recommendations based on hotspot intensity and trend projections.
- **Exportable PDF Reports:** One-click executive reporting for precinct leadership.

---

## Installation & Setup

### Prerequisites
- Python 3.9+ or Python 3.10+
- Java JRE 11+ (required for H2O AutoML dependencies)

### Local Environment Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VishalKumar-S/Predictive_Guardians.git CrimeNexus
   cd CrimeNexus
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install pinned dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   streamlit run app/app.py
   ```

---

## Containerization (Docker)

To build and execute inside Docker container:

```bash
docker build -t crime-nexus:latest .
docker run -p 8501:8501 crime-nexus:latest
```

Open your browser at `http://localhost:8501`.

---

## Project Governance Documents
All project governance decision records and impact assessments are available in `docs/governance/`:
- [Ethical AI & Bias Impact Assessment](docs/governance/ethical_ai_impact_assessment.md) ([Root Link](ethical_ai_impact_assessment.md))
- [Data Licensing & Fallback Catalog](docs/governance/data_licensing_catalog.md) ([Root Link](data_licensing_catalog.md))
- [Team Roster](docs/governance/team_roster.md)
- [Legal Opinion Memo](docs/governance/legal_opinion_memo.md)
- [Decision Record: Caste Removal](docs/governance/decision_record_caste_removal.md)
- [Decision Record: Recidivism Scope](docs/governance/recidivism_scope_decision.md)
- [Decision Record: Data Source](docs/governance/data_source_decision.md)
- [Data Privacy & PII Handling Policy](docs/governance/data_privacy_policy.md)

