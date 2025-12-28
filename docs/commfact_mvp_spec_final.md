# COMMFACT Lite — MVP Specification (Final)

**Version:** 1.0 (Locked)  
**Status:** Tier 1 Pilot–Ready  
**Purpose:** This document formally locks the scope, principles, and operating assumptions of the COMMFACT Lite MVP.

---

## 1. Product Definition

**COMMFACT Lite** is a communication governance and accountability system designed to **identify normative risk in public communication before publication**, while preserving **human decision authority**.

The system:
- does **not** generate content
- does **not** make legal determinations
- does **not** replace professional judgement

Its primary function is to **surface risk signals, document decisions, and preserve accountability**.

---

## 2. Core Principles (Non-Negotiable)

1. **Governance before creativity**  
   Communication quality is secondary to accountability and responsibility.

2. **Rules before intuition**  
   Risk identification must be grounded in explicit, shared norms.

3. **Human accountability remains final**  
   All approvals, rejections, and revisions are owned by named human actors.

4. **Explainability over automation**  
   Every rule and outcome must be understandable without technical expertise.

---

## 3. Locked Scope

### 3.1 Included in MVP

- Rule-based risk identification (Tier 1)
- Explicit rule taxonomy (v1.0)
- Transparent rule catalog with regulatory alignment
- Manual human decision submission
- Immutable audit logging (content ID, role, decision, timestamp)
- Basic UI for validation and review

---

### 3.2 Explicitly Excluded

The following are **out of scope** for the MVP:

- Content generation or rewriting
- Automatic approval or rejection
- Recommendation lists or optimisation advice
- Sentiment analysis or brand tone checks
- Jurisdiction-specific legal verdicts
- Client-specific custom rules

These exclusions are deliberate and strategic.

---

## 4. Rule System Overview

- Rules are organised under **Rule Taxonomy v1.0**
- Each rule has:
  - a unique ID
  - category and severity
  - normative regulatory basis
  - indicative linguistic triggers

Rules identify **risk categories**, not violations.

---

## 5. Governance & Accountability Model

### 5.1 System Roles

- **Creator** — submits content
- **Reviewer** — evaluates flagged risk and submits decisions
- **System** — logs validation results and decisions

---

### 5.2 Decision Authority

- The system **cannot approve or reject content**
- All decisions require explicit human action
- Severity determines review strictness, not outcome

---

### 5.3 Audit Log

Each decision records:
- content identifier
- actor role
- decision outcome
- justification / reason
- triggered rule IDs
- timestamp

Audit logs are append-only.

---

## 6. Adoption Assumptions (Tier 1)

The MVP is designed for:
- regulated or reputation-sensitive agencies
- internal governance pilots
- reviewer-led workflows

Success is defined by **use**, not automation.

---

## 7. Success Metrics (MVP-Level)

- Consistent reviewer usage
- Decision trace completeness
- Rule transparency acceptance by agencies
- No automated decisions occurring

Revenue, scale, and optimisation are **explicitly out of scope** at this stage.

---

## 8. Change Control

- This MVP spec is **locked** for Tier 1 pilots
- No scope expansion during pilot phase
- Any changes require:
  - documented rationale
  - governance review
  - version increment

---

## 9. Positioning Statement

> COMMFACT Lite is not an AI that decides.
> It is a system that **forces decisions to be visible, justifiable, and owned**.

---

**Final Lock Statement**  
This document represents the final agreed specification of the COMMFACT Lite MVP.  
No features, behaviours, or claims outside this document are considered part of the MVP.

