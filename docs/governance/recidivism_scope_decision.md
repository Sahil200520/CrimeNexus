# Decision Record: Recidivism Prediction Module Scope & Fate

**Decision Record ID:** ADR-2026-02  
**Status:** Approved (Research-Only Track Enforced)  
**Date:** Wednesday, August 19, 2026  
**Signatories:** Project Manager, ML Lead, Project Sponsor  

---

## Context & Evaluation

The recidivism prediction module (repeat offense estimation) poses high risk regarding individual profiling, false positive rates, and algorithmic bias if deployed in operational law enforcement workflows without extensive explainability safeguards.

---

## Scope Decision

1. **Research-Only Track (Default):**
   - The Recidivism Prediction module is classified as **Research-Only / Proof-of-Concept**.
   - It will be strictly isolated behind a `RESEARCH_MODE_ENABLED` configuration flag in code.
   - It will **not** be presented in standard operational law enforcement UI dashboards or patrol allocation workflows.

2. **Production Track Criteria (Conditional):**
   - Transfer of the recidivism module to production track requires:
     a) Full replacement of black-box models (e.g. default H2O AutoML) with interpretable models (e.g. Logistic Regression / Explainable Boosting) accompanied by SHAP feature explanations (scheduled for Week 6 if approved).
     b) Formal algorithmic bias audit sign-off by an independent auditor.

---

## Code Enforcements
- In `app.py`, recidivism tabs will display an explicit badge: `[RESEARCH ONLY — NOT FOR OPERATIONAL DECISION MAKING]`.

---

**Signed:**  
*Project Manager & ML Lead*
