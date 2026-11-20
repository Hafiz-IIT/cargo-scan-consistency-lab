# Methodology and limitations

This repository contains two deterministic prototypes:
1. A declared-versus-observed cargo record comparator.
2. A categorical sensor-fusion heuristic that groups observations by caller-supplied independence labels and avoids double-counting multiple channels from one group.

Synthetic scenarios are generated from a fixed seed. They are fictional fixtures, not real scanner data, cargo manifests, customs records or measured sensor outputs.

## Interpretation
- A discrepancy indicates that configured fields differ beyond configured tolerances.
- A fusion result marked for review indicates insufficient group support, low support, category disagreement or disagreement within a shared group.
- An independent_group label is a caller assertion; it does not prove statistical independence, distinct hardware, separate administrators or separate trust roots.
- Confidence values are inputs, not calibrated probabilities.

## Limitations
The comparator checks only category, weight, dimensions and seal state. The fusion heuristic is not a Bayesian model, calibrated classifier or customs decision engine. It does not parse images, validate sensor calibration, verify sensor identity, or establish the truth of a cargo declaration.
