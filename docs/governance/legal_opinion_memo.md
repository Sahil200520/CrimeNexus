# Legal Opinion Memo: Caste-Based Crime Statistics & Machine Learning Compliance

**To:** Project Steering Committee & Sponsor  
**From:** Legal & Ethics Compliance Officer  
**Date:** Tuesday, August 18, 2026  
**Subject:** Statutory Evaluation of Caste Features in Predictive Policing & Criminal Profiling Algorithms  

---

## Executive Summary

This memorandum provides a binding legal evaluation regarding the ingestion, processing, and visual display of caste-based demographic attributes within the **Crime Hotspot Mapping & Behavioural Analysis System (CT-DFIR-01)**. 

Following comprehensive analysis under the **Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989** (and subsequent amendments), **Article 15 of the Constitution of India**, and national data privacy standards, **it is the opinion of Legal Counsel that all caste-based attributes must be immediately and permanently removed** from model feature sets, analytics charts, profiling algorithms, and UI displays.

---

## Statutory & Constitutional Framework

1. **Article 15(1), Constitution of India:**
   - Prohibition of discrimination on grounds of religion, race, caste, sex, or place of birth. Machine learning algorithms that utilize caste as a predictor for recidivism, criminal propensity, or risk profiling violate constitutional non-discrimination principles.

2. **Scheduled Castes and the Scheduled Tribes (Prevention of Atrocities) Act, 1989:**
   - Inclusion of caste attributes in predictive policing algorithms risks institutionalizing algorithmic bias, profiling marginalized communities, and causing systemic harm, exposing automated systems and operators to legal challenge and administrative invalidation.

3. **Data Protection & Ethics Directives:**
   - Protected social attributes cannot serve as inputs for law enforcement predictive modeling unless explicitly mandated by statutory crime reporting rules (strictly isolated to post-incident statistical reporting, never predictive modeling).

---

## Directives for Project Codebase

1. **Model Training Pipelines:**
   - Immediately drop `Caste` columns from all feature matrices, training routines (`ingest_data.py`, `train_model.py`), and evaluation benchmarks.

2. **Analytics & Visualization:**
   - Remove caste distribution charts, demographic breakdowns by caste, and related filters from the frontend web application.

3. **Data Schemas:**
   - Purge caste variables from transformed datasets and synthetic FIR schemas prior to Phase 1 close.

---

**Approved by:**  
*Legal & Ethics Compliance Lead*  
*CT-DFIR-01 Project Governance Gate*
