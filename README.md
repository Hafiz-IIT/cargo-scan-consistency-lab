# Cargo Scan Consistency Lab

A transparent synthetic consistency checker comparing declared shipment attributes with observed/sensor-side evidence.

## Implemented
- declared vs observed cargo category
- absolute/relative weight mismatch
- dimension tolerance checks
- seal-state comparison
- discrepancy report with severity
- explicit human-review recommendation
- deterministic tests

## Important boundary
This repository does **not** claim to perform real X-ray, IR, RF or customs-scanner interpretation. Observations are structured synthetic inputs so the decision logic can be tested independently of unavailable hardware/model pipelines.
