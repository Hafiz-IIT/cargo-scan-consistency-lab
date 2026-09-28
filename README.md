# Cargo Scan Consistency Lab

> Synthetic cargo-evidence consistency lab comparing declarations with structured scanner/sensor-side observations.

## Status
**Reproducible prototype** with executable Python, tests, and GitHub Actions CI.

## Problem
A shipment declaration can be internally consistent while physical evidence points elsewhere. The decision layer needs explicit discrepancy handling rather than blind trust in either source.

## Architecture
Declared cargo record + observed cargo record → category/weight/dimension/seal comparisons → tolerance checks → discrepancy severity → human-review signal.

## Quick start
```bash
python -m unittest discover -s tests -v
python cargo_scan_consistency_lab.py
```

## Implemented
- Structured declared/observed records
- Category mismatch detection
- Relative weight tolerance
- Dimension tolerances
- Seal-state comparison
- Severity labels
- Human-review trigger
- Tests and CI

## Research lineage
- *AI for Supply Chain Integrity*
- *Ethical & Legal Dimensions of Autonomous Systems*
- *Human-Centered AI Design for Inclusive Digital Platforms*

## Evaluation
Tests verify clean matches and obvious mismatches; future experiments should add sensor noise and threshold calibration.

## Limitations
- No X-ray/IR/RF interpretation model
- No scanner hardware
- Synthetic structured observations only
- No customs deployment claim

## License
MIT.

## Extended implementation

- `multimodal_fusion.py` — provenance-aware categorical fusion that avoids double-counting correlated evidence channels.
- `synthetic_scenarios.py` — reproducible synthetic declaration/observation cases.
- `paper/EXIM_MULTIMODAL_FRAMEWORK.md` — working manuscript scaffold with explicit hardware/regulatory non-claims.
- `docs/SENSOR_BOUNDARIES.md` — public physical-sensing boundary.
