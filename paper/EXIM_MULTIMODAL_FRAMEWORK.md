# EXIM AI Co-Pilot: A Multimodal Cargo Scanning & Customs Automation Framework

**Working manuscript — concept + software prototype. Not submitted or published.**

## Abstract
This manuscript studies a software architecture for comparing shipment declarations with heterogeneous physical-side evidence before an automated trade system authorizes consequential workflow actions. The public prototype deliberately avoids claims of operational X-ray, terahertz, infrared, radio-frequency, or customs-scanner deployment. Instead, it evaluates transparent evidence-consistency rules using synthetic cargo attributes and simulated modality outputs. The central question is whether provenance-aware multimodal agreement, explicit conflict handling, and human-review escalation can provide a safer interface between document automation and future physical sensing systems.

## 1. Motivation
EXIM workflows combine documents, declarations, logistics events and, in some settings, physical inspection. A reliable system must distinguish:
- a document that was parsed correctly,
- evidence sources that actually agree,
- evidence sources that are independent,
- and a case that is safe enough to automate.

## 2. Proposed architecture
1. Declaration/document layer
2. Structured cargo attributes
3. Optional physical/sensor adapters
4. Provenance and independence labels
5. Multimodal evidence fusion
6. Discrepancy severity
7. ACT / VERIFY / ESCALATE workflow gate
8. Human review and audit trail

## 3. Public implementation
The repository currently implements:
- declaration-vs-observation consistency checks;
- configurable tolerances for weight/dimensions;
- seal-state and category discrepancies;
- provenance-aware categorical evidence fusion;
- synthetic scenario generation;
- deterministic tests.

## 4. Explicit non-claims
The repository does **not** contain:
- operational scanner hardware;
- radiation-source control;
- calibrated X-ray/terahertz/hyperspectral models;
- real customs records;
- ICEGATE/DGFT credentials;
- validation on live cargo.

## 5. Experimental questions
- Does source-independence accounting reduce false confidence from correlated sensors?
- How does conflict-aware review affect false-clearance vs unnecessary-review trade-offs?
- Which discrepancy families are most likely to cascade into unsafe downstream actions?
- How robust are thresholds to noise and missing channels?

## 6. Planned evaluation
Synthetic cases will vary:
- declaration correctness;
- weight and dimension mismatch;
- category mismatch;
- seal integrity;
- missing modalities;
- correlated modalities;
- confidence miscalibration;
- adversarial agreement.

Metrics: false-clearance rate, review rate, mismatch recall, source-diversity sensitivity, and calibration.

## 7. Safety and regulatory boundary
Any real radiation-emitting inspection system requires qualified engineering, radiation-safety analysis, regulatory approval, shielding, equipment certification and item-specific validation. This manuscript intentionally does not prescribe exposure levels or operational scanner settings.

## 8. Relationship to the wider EXIM project
This is a research slice of the broader EXIM AI Co-Pilot concept: a unified workflow for document intelligence, compliance support, logistics coordination, discrepancy detection, evidence-gated automation and role-specific dashboards.

## 9. Future work
- permissioned real-data evaluation;
- calibrated modality reliability;
- image/sensor adapters;
- human-review study;
- integration with the document-truth benchmark and evidence-gated autonomy layer.

## 10. Publication rule
A preprint should only be submitted after experiments are frozen, results are generated, related work is properly cited, and all claims are aligned with measured evidence.
