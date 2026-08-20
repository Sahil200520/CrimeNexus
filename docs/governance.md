# Crime Nexus (CT-DFIR-01) — System Governance & Ethics Master Framework

> **Document Status**: Active / Mandatory System Governance Master Index  
> **Applicability**: All modules, dataset ingestors, ML pipelines, and user interfaces across CT-DFIR-01  
> **Primary Authority**: Project Sponsor, Legal Counsel, Lead Ethics Officer  

---

## 1. Governance Architecture Overview

The **Crime Nexus (CT-DFIR-01)** platform is bound by strict ethical AI standards, legal non-discrimination mandates, privacy laws, and intellectual property requirements. 

This master document serves as the central index and authoritative framework governing all system development, data ingestion, predictive modeling, and law enforcement advisory usage.

```
                                  ┌───────────────────────────────────┐
                                  │   docs/governance.md (Master)     │
                                  └─────────────────┬─────────────────┘
                                                    │
         ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
         │                                          │                                          │
┌────────┴──────────────────────────┐    ┌──────────┴──────────────────────────┐    ┌──────────┴──────────────────────────┐
│ Ethical AI & Human-in-the-Loop    │    │ Statutory & Legal Non-Discrimination│    │ Privacy & Data Governance           │
├───────────────────────────────────┤    ├─────────────────────────────────────┤    ├─────────────────────────────────────┤
│ • ethical_ai_impact_assessment.md │    │ • decision_record_caste_removal.md  │    │ • data_privacy_policy.md            │
│ • recidivism_scope_decision.md    │    │ • legal_opinion_memo.md             │    │ • data_licensing_catalog.md         │
└───────────────────────────────────┘    └─────────────────────────────────────┘    │ • data_source_decision.md           │
                                                                                    └─────────────────────────────────────┘
```

---

## 2. Governance Document Registry

All binding governance decision records, impact assessments, and legal policy memos are stored in [`docs/governance/`](file:///c:/Users/aswin/Desktop/CrimeNexus/docs/governance/):

| Document | Purpose & Key Mandate | Status |
| :--- | :--- | :--- |
| 🛡️ [**Ethical AI & Bias Impact Assessment**](governance/ethical_ai_impact_assessment.md) | Proves model is strictly for **Decision Support (Human-in-the-Loop)**. Expressly prohibits automated arrests, predictive suspect profiling, or automated dispatch. | **Approved** ✅ |
| 📜 [**Data Licensing & Fallback Catalog**](governance/data_licensing_catalog.md) | Inventory of GeoJSON maps, FIR data, and iRAD accident data sources, licenses (OGD, ODbL, CC0), and 100% offline fallback rules. | **Approved** ✅ |
| ⚖️ [**Decision Record: Caste Removal**](governance/decision_record_caste_removal.md) | ADR-2026-01: Mandatory 100% excision of `Caste` and protected demographic attributes from ingestion pipelines, models, and UI under SC/ST Act compliance. | **Approved** ✅ |
| 🔬 [**Decision Record: Recidivism Scope**](governance/recidivism_scope_decision.md) | ADR-2026-02: Isolates recidivism scoring strictly to research evaluation (`RESEARCH_MODE_ENABLED=true`) with non-operational watermarks. | **Approved** ✅ |
| 📊 [**Decision Record: Synthetic Data Source**](governance/data_source_decision.md) | ADR-2026-03: Governs the usage of realistic synthetic FIR records for safe PoC analytics without exposing live operational PII. | **Approved** ✅ |
| 🔒 [**Data Privacy & PII Policy**](governance/data_privacy_policy.md) | Enforces SHA-256 name hashing, contact masking, and $\pm 500\text{m}$ spatial coordinate jittering under DPDP Act 2023. | **Approved** ✅ |
| ⚖️ [**Legal Opinion Memo**](governance/legal_opinion_memo.md) | Formal legal counsel memo establishing compliance with Constitution Articles 15/21, SC/ST Act 1989, and privacy jurisprudence. | **Approved** ✅ |
| 👥 [**Team Roster & Roles**](governance/team_roster.md) | Roster of project leads, ethics officers, and technical leads responsible for governance enforcement. | **Active** ✅ |

---

## 3. Core Operational Directives

### Directive 1: Human-in-the-Loop (HITL) Imperative
- **No Automated Action**: Machine learning outputs (hotspots, risk scores, patrol route recommendations) are purely advisory.
- **Mandatory Officer Sign-Off**: Field dispatch or patrol deployments require explicit manual authorization by a human police officer.
- **Auditability**: Officer overrides and acceptances are logged in an immutable audit trail.

### Directive 2: Complete Excision of Protected Attributes
- **Zero Demographic Features**: `Caste`, `Religion`, `Community`, `Socio-Economic Class`, and `Gender` are barred from all model training sets and analytics visualizations.
- **Ingestion Audit**: Pipelines (such as `Criminal_Profiling/ingest_data.py`) must drop protected attributes prior to feature processing.

### Directive 3: Data Privacy & Anonymization
- **SHA-256 Hashing**: Citizen and complainant names are hashed with `ANONYMIZATION_SALT`.
- **Spatial Jittering**: Coordinates in FIR records are jittered by $\pm 500\text{m}$ to prevent geographic stigmatization of specific neighborhoods.

### Directive 4: Offline Resilience & Licensing
- **Zero External Internet Dependency**: All spatial GeoJSON layers and crime databases must operate offline using pre-packaged local fallbacks (`assets/geojson/`, `data/crime_nexus.db`).

---

## 4. Escalation & Audit Protocols

1. **Pull Request Validation**: Any code change introducing protected characteristic features or bypassing PII hashing will trigger an immediate build rejection.
2. **Periodic Audits**: Quarterly disparate impact ratio (DIR) checks across spatial precincts to prevent over-policing bias.
3. **Grievance Logging**: Community and user feedback logged via `Continuous_learning_and_feedback` triggers automated alert notifications if bias or system thresholds are approached.
