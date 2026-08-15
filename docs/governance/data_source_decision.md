# Decision Record: Real KSP Data vs. Synthetic Dataset for Public Build

**Decision Record ID:** ADR-2026-03  
**Status:** Approved (Synthetic Dataset Selected)  
**Date:** Wednesday, August 19, 2026  
**Signatories:** Project Manager, Data Engineer, Stakeholder Lead  

---

## Context & Security Considerations

Deploying or hosting real law enforcement FIR records (e.g. Karnataka State Police / KSP datasets containing identifiable personal information, victim addresses, and ongoing investigation details) in a public repository or web demonstration creates severe privacy vulnerabilities, confidentiality breaches, and legal liabilities.

---

## Decision Taken

1. **Synthetic Data for Public Demonstrations & Builds:**
   - The public repository and demonstration app will exclusively utilize a **realistically formatted synthetic FIR dataset**.
   - The synthetic dataset schema will mirror actual FIR structures (IPC/NDPS/Arms Act sections, spatial coordinates, time/season attributes, district units) without containing real PII (Personally Identifiable Information).

2. **Schema & Licensing Specification:**
   - Synthetic FIR schema design will take place during Week 3 (Phase 1 close) and be populated in Week 4.
   - All external geographical boundaries (GeoJSON) and secondary data (iRAD accident zones) will be documented with explicit licensing and local fallbacks.

3. **Operational Adapter:**
   - An isolated data ingestion connector will be provided for law enforcement deployments to bind real database tables securely behind enterprise firewalls.

---

**Signed:**  
*Project Manager & Data Engineering Lead*
