# Architecture

```mermaid
flowchart LR
    N0[declared cargo] --> N1
    N1[structured observations] --> N2
    N2[tolerance checks] --> N3
    N3[discrepancy list] --> N4
    N4[severity] --> N5
    N5[human review]
```

## Declaration
Structured shipment attributes form the expected state.

## Observation
Synthetic structured measurements represent what a future sensing stack might output.

## Comparator
Field-specific tolerances convert differences into discrepancies.

## Review gate
Any discrepancy currently requires review; future work can calibrate severity/risk thresholds.

## Design principle
Keep physical evidence comparison separate from the unbuilt perception stack so evaluation claims remain honest.
