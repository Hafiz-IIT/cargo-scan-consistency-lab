# Architecture

Declared cargo record + observed cargo record → category/weight/dimension/seal comparisons → tolerance checks → discrepancy severity → human-review signal.

## Invariants
1. Observed/declaration mismatches must be explicit.
2. Tolerance thresholds must be configurable.
3. Any detected discrepancy must be reviewable rather than silently overwritten.

## Integration rule
Future external adapters must not discard provenance, access-control decisions, uncertainty, or failure states.
