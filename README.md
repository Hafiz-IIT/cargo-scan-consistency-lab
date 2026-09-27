# Cargo Scan Consistency Lab

> **Compare what a shipment declares with what structured physical-side evidence observes—then escalate discrepancies.**

The historical EXIM AI vision extended verification beyond documents: declared cargo attributes should eventually be compared against scanner/sensor/weight evidence. This repository implements only the transparent consistency layer so the logic can be evaluated without pretending unavailable X-ray/RF/IR hardware exists.

## Implemented
- declared and observed cargo records
- category mismatch detection
- relative weight-tolerance checks
- dimension-tolerance checks
- seal-state comparison
- severity-tagged discrepancies
- human-review trigger

## Structure
- `cargo_scan_consistency_lab.py` — core
- `tests/` — tests
- `examples/` — reproducible example
- `docs/architecture.md` — architecture
- `docs/research-agenda.md` — experiments + manuscript lineage
- `STATUS.md` — maturity/claims
- `CITATION.cff` — citation metadata

## Run
```bash
python -m unittest discover -s tests -v
python cargo_scan_consistency_lab.py
```

## Pipeline
**declared cargo → structured observations → tolerance checks → discrepancy list → severity → human review**

## Research lineage
Directly linked to the EXIM AI multimodal cargo-scanning concept discussed for X-ray, RF, infrared, weight, and declaration/RITC consistency. The present code deliberately stops before image/sensor interpretation.

## Evaluation
Stress weight/dimension/category/seal deviations at controlled magnitudes and measure detection thresholds, escalation burden, and sensitivity to noisy observations.

## Maturity
**Research prototype.** No real X-ray, IR, RF, computer-vision model, customs scanner, RITC classifier, or field sensor is implemented or claimed.
