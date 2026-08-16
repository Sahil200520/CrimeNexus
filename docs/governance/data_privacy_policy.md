# Data Privacy & PII Handling Policy

**Document ID:** POL-2026-DP01  
**Project:** Crime Hotspot Mapping & Behavioural Analysis System (CT-DFIR-01)  
**Effective Date:** Monday, August 17, 2026  
**Status:** Mandatory & Binding  
**Scope:** All dataset ingestion pipelines, synthetic data generators, storage databases, and application interfaces.

---

## 1. Objective & Legal Basis

This policy defines mandatory protocols for safeguarding **Personally Identifiable Information (PII)** contained within First Information Reports (FIRs), offender records, complainant logs, and spatial location data. 

All technical implementations must comply with the **Digital Personal Data Protection (DPDP) Act**, national security guidelines, and SC/ST Act non-discrimination mandates.

---

## 2. PII Classification Matrix

| Attribute Category | Fields Included | Handling Standard | Technical Action Required |
|---|---|---|---|
| **Direct PII** | Complainant Name, Accused Name, Victim Name, Phone Number, Aadhaar / National ID | **STRICT PROHIBITION** | Complete masking, hashing (SHA-256 with salt), or synthetic replacement (e.g., `ACC_SYNTH_8402`). |
| **Granular Spatial PII** | Exact House Address, Door Number, Street Name, Micro Coordinates | **SUPPRESSION / GENERALIZATION** | Spatial jittering ($\pm 500\text{m}$ grid resolution) or aggregation to Police Station / District Unit level. |
| **Protected Demographics** | Caste, Sub-Caste, Tribe, Community, Religion | **100% EXCISION** | Complete removal from ingestion pipelines (`ingest_data.py`), model feature matrices, and UI charts. |
| **Allowable Analytics Attributes** | Incident Type (IPC/NDPS/Arms Act), Date, Time, District Unit, General Incident Locality | **ANALYTICS PERMITTED** | Retained for spatio-temporal clustering and seasonal trend forecasting. |

---

## 3. Mandatory Engineering Rules

### Rule 3.1: Anonymization at Ingestion Boundary
No raw, un-masked PII shall pass beyond the data ingestion boundary.
- **Implementation:** Ingestion scripts (`ingest_data.py` / `transform_data.py`) must strip or hash name columns before saving dataframe artifacts.

### Rule 3.2: Spatial Masking for Visualizations
Coordinates plotted on public maps (Choropleth/Heatmap) must be jittered or aggregated to protect individual premises privacy:
$$\text{Lat}_{\text{masked}} = \text{Lat} + \delta_{\text{lat}}, \quad \text{Lon}_{\text{masked}} = \text{Lon} + \delta_{\text{lon}}$$
where $\delta \sim \mathcal{U}(-0.005, 0.005)$ ($\approx \pm 500\text{m}$).

### Rule 3.3: Zero Hardcoded Credentials & PII Logs
- Application logs must never write plain-text names, passwords, or contact records to stdout, stderr, or disk log files.
- Secrets must be loaded exclusively via environment variables (`.env`).

### Rule 3.4: Synthetic Data Standard for Demonstration
Demonstration and public builds must exclusively consume synthetic datasets built on randomized identity schemas.

---

## 4. Compliance Auditing

- **Pre-Commit Verification:** Code commits modifying data ingestion routines must verify zero PII leakage.
- **Phase Gate Review:** Data Engineer & Ethics Officer must sign off on dataset compliance before Phase 1 close.

---

**Approved by:**  
*Legal & Ethics Officer*  
*Data Engineering Lead*  
*Project Manager*
