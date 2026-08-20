# Ethical AI & Bias Impact Assessment (CT-DFIR-01)

> **Document Status**: Approved / Mandatory Governance Standard  
> **Target Platform**: Crime Nexus (CT-DFIR-01)  
> **Primary Directive**: Human-in-the-Loop (HITL) Decision Support Only — Zero Automated Enforcement  

---

## 1. Executive Summary & Core Mandate

This **Ethical AI & Bias Impact Assessment** formally certifies that the **Crime Nexus (CT-DFIR-01)** system is designed, architected, and operated **strictly as a Decision Support System (DSS)** and an analytical advisory framework. 

The system provides spatial-temporal hotspot mapping, legal section tagging, and patrol route optimization to assist police commanders and law enforcement analysts in resource allocation. **Under no circumstances does Crime Nexus perform, authorize, or automate any law enforcement actions.**

### 🛑 Strict System Prohibitions
1. **NO Automated Arrests or Warrants**: The system has zero capability or interface to initiate, issue, or execute arrest warrants or detentions.
2. **NO Individual Predictive Profiling**: The system does NOT score, target, rank, or track individual citizens or suspect identities for predictive intervention.
3. **NO Automated Dispatch or Deployment**: Machine learning recommendations (e.g., patrol routes) are purely advisory proposals requiring explicit human authorization.
4. **NO Demographically Biased Input Features**: Features such as caste, religion, ethnicity, gender, community origin, or socio-economic indicators are strictly excised from all models.

---

## 2. Human-in-the-Loop (HITL) Architecture

Crime Nexus mandates a **Three-Tier Human-in-the-Loop (HITL)** operational workflow. No machine output directly triggers field activity without passing through human evaluation and authorization.

```
┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│   Level 1: AI Engine    │ ──> │ Level 2: Analyst Review │ ──> │ Level 3: Commander Auth │
│ Spatial Pattern Scoring │     │ Spatial Context & Logs  │     │ Field Dispatch & Orders │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘
```

### Operational Oversight Tiers
* **Level 1 (Algorithmic Proposal)**: The ML model analyzes historical spatial-temporal incident patterns and outputs advisory hotspot maps and route suggestions.
* **Level 2 (Analytical Validation)**: A trained crime analyst or precinct officer reviews the proposal against real-time local context (e.g., local events, construction, weather, active community gatherings).
* **Level 3 (Command Authorization)**: A senior police officer explicitly signs off on, modifies, or rejects the recommended patrol deployment.

### Immutable Audit Trail & Override Logging
- Every interaction with AI-generated recommendations (accepted, modified, or overridden) is recorded in an immutable SQLite/PostgreSQL audit database.
- Officers are required to document the operational rationale whenever overriding an AI recommendation, ensuring full accountability.

---

## 3. Bias Eradication & Statutory Compliance

### Constitutional & Statutory Safeguards
Crime Nexus strictly adheres to the legal frameworks governing equality, non-discrimination, and fundamental rights in India:
- **Article 15 of the Constitution of India**: Prohibition of discrimination on grounds of religion, race, caste, sex, or place of birth.
- **Article 21 of the Constitution of India**: Protection of life and personal liberty, including personal privacy.
- **SC/ST (Prevention of Atrocities) Act, 1989**: Absolute bar against racial, caste-based, or community-based profiling.
- **Digital Personal Data Protection (DPDP) Act, 2023**: Mandatory anonymization, storage limitation, and purpose restriction.

### Mitigation Strategies Implemented
1. **Demographic Excision**: All protected characteristics (caste, religion, tribe, socio-economic class) are purged during data ingestion. Models operate solely on spatial, temporal, environmental, and incident category features.
2. **Spatial Coordinate Jittering ($\pm 500\text{m}$)**: Incident coordinates in FIR records undergo spatial jittering prior to visualization or modeling to prevent geographic stigmatization of specific neighborhoods or residential blocks.
3. **PII Anonymization & Hashing**: Names of complainants, victims, and witnesses are hashed using SHA-256 with a unique salt (`ANONYMIZATION_SALT`). Contact numbers and addresses are masked.

---

## 4. Research-Only Scope for Sensitive Modules

### Recidivism Scoring Isolation
The recidivism evaluation module is strictly isolated under a **Research-Only** configuration flag:

```env
RESEARCH_MODE_ENABLED=true
```

- When `RESEARCH_MODE_ENABLED=true`, recidivism modeling functions exclusively as a sandboxed statistical benchmark for academic and policy evaluation.
- Outputs from the recidivism module are **watermarked** as `RESEARCH ONLY - NOT FOR OPERATIONAL USE` and cannot be fed into active dispatch or patrol route generators.

---

## 5. Explainable AI (XAI) & Transparency Standards

To combat "black-box" decision-making, Crime Nexus incorporates explainability standards into all analytical views:

- **Feature Attribution**: Spatial hotspot intensity is accompanied by feature importance metrics (e.g., SHAP values), highlighting key drivers such as temporal density, historical incident frequency, or seasonal factors.
- **Uncertainty Quantification**: Model predictions present confidence intervals and variance estimates, alerting analysts when spatial data density is insufficient to draw reliable conclusions.
- **Clear Limitations Warning**: Every generated report displays prominent disclaimers emphasizing that historical data reflects recorded incidents, not absolute crime rates.

---

## 6. Continuous Bias Auditing & Recourse Mechanism

### Periodic Disparate Impact Audits
Crime Nexus enforces quarterly algorithmic audits to evaluate model fairness across spatial zones:
- **Disparate Impact Ratio (DIR)**: Evaluates whether patrol route recommendations disproportionately over-index in specific socio-economic precincts relative to recorded incident frequency.
- **False Positive Rate Equality**: Ensures model error rates are uniform across administrative zones.

### Citizen Recourse & Grievance Alignment
- Any community feedback or grievance regarding over-policing or spatial misallocation is logged in the `Continuous_learning_and_feedback` module.
- Automated threshold alerts (`send_alert`) notify the engineering and command team if user ratings or feedback flag potential bias or operational issues.

---

## 7. Sign-off & Certification

| Role | Responsibility | Status |
| :--- | :--- | :--- |
| **Lead AI Ethics Officer** | Algorithmic Bias & HITL Protocol Audit | Approved ✅ |
| **Legal Counsel** | Constitutional & SC/ST Act Compliance Verification | Approved ✅ |
| **Project Lead** | System Purpose & Scope Enforcement | Approved ✅ |
