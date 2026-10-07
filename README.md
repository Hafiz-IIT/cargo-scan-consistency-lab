# Cargo Scan Consistency Lab

<p align="center"><strong>Declaration vs Observation: A Synthetic Cargo-Evidence Lab</strong><br/><sub>Model discrepancies explicitly before they become operational decisions.</sub></p>

<p align="center"><a href="https://github.com/Hafiz-IIT/cargo-scan-consistency-lab/actions"><img src="https://img.shields.io/github/actions/workflow/status/Hafiz-IIT/cargo-scan-consistency-lab/ci.yml?label=CI" alt="CI"/></a> <img src="https://img.shields.io/badge/status-reproducible%20prototype-blue" alt="Prototype"/></p>

## Research question

**How should an AI system report disagreement between a shipment declaration and observed cargo evidence without pretending the observation source is infallible?**

## Pipeline

```
Declared record + observed record
              ↓
 category / weight / dimensions / seal
              ↓
       tolerance checks
              ↓
      discrepancy severity
              ↓
        review signal
```

## Try it

```bash
python cargo_scan_consistency_lab.py
python -m unittest discover -s tests -v
```

Additional modules include provenance-aware multimodal fusion and synthetic scenarios.

## Implemented

- declared/observed structured records
- category mismatch detection
- weight and dimension tolerances
- seal-state comparison
- discrepancy severity
- provenance-aware evidence fusion
- synthetic scenarios
- deterministic CI

## Critical boundary

**This repository does not implement an X-ray, IR, RF, THz or physical cargo scanner.** It models structured observations so the decision layer can be studied independently of hardware.

Related: [EXIM Document Truth Bench](https://github.com/Hafiz-IIT/exim-document-truth-bench) · [EXIM Copilot Core](https://github.com/Hafiz-IIT/exim-copilot-core)
