# Formal Decision Record: Complete Excise of Caste Analysis

**Decision Record ID:** ADR-2026-01  
**Status:** Approved & Binding  
**Date:** Tuesday, August 18, 2026  
**Signatories:** Project Manager, Legal & Ethics Officer, Project Sponsor  

---

## Context & Problem Statement

The inherited repository (`Predictive_Guardians`) included `Caste` as a column in dataset ingestion routines (`Criminal_Profiling/ingest_data.py`) and potential feature inputs for criminal profiling. Incorporating protected attributes creates unacceptable ethical risks of algorithmic bias, discriminative profiling, and statutory non-compliance.

---

## Decision Taken

1. **Total Removal of Caste Feature:**
   - Caste data will be **100% removed** as both a predictive model feature and an analytics visualization chart across all components of CT-DFIR-01.
   - Codebase refactoring will be executed during Week 3 as part of Phase 1 closure.

2. **Escalation Protocol:**
   - Any pull request or commit re-introducing protected characteristic variables (caste, religion, tribe) will trigger an automatic build failure in CI/CD and require immediate legal review.

3. **Auditability:**
   - Week 6 will feature a mandatory ethics checklist audit verifying zero protected-characteristic inputs in all active models.

---

## Signatures

- **Project Manager:** *Signed*
- **Project Sponsor:** *Signed*
- **Legal & Ethics Officer:** *Signed*
