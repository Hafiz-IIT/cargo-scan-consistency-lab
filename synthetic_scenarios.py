from __future__ import annotations

from dataclasses import asdict
import json
import random

from cargo_scan_consistency_lab import CargoRecord


CATEGORIES = ("textiles", "electronics", "machinery", "food")


def generate_scenarios(n: int = 100, *, seed: int = 7, anomaly_rate: float = 0.25) -> list[dict]:
    """Generate reproducible synthetic declaration/observation pairs.

    No real customs, scanner, or commercial data is used.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    if not 0 <= anomaly_rate <= 1:
        raise ValueError("anomaly_rate must be between 0 and 1")

    rng = random.Random(seed)
    rows: list[dict] = []

    for i in range(n):
        category = rng.choice(CATEGORIES)
        weight = rng.uniform(100.0, 5000.0)
        dims = [rng.uniform(40.0, 250.0) for _ in range(3)]
        declared = CargoRecord(category, weight, *dims, True)

        anomalous = rng.random() < anomaly_rate
        observed_category = category
        observed_weight = weight
        observed_dims = dims[:]
        observed_seal = True
        anomaly_types: list[str] = []

        if anomalous:
            kind = rng.choice(("category", "weight", "dimension", "seal"))
            anomaly_types.append(kind)
            if kind == "category":
                observed_category = rng.choice([c for c in CATEGORIES if c != category])
            elif kind == "weight":
                observed_weight *= rng.choice((0.80, 1.20))
            elif kind == "dimension":
                j = rng.randrange(3)
                observed_dims[j] *= 1.25
            else:
                observed_seal = False

        observed = CargoRecord(
            observed_category,
            observed_weight,
            *observed_dims,
            observed_seal,
        )
        rows.append({
            "scenario_id": f"S{i:04d}",
            "declared": asdict(declared),
            "observed": asdict(observed),
            "anomaly_types": anomaly_types,
        })

    return rows


if __name__ == "__main__":
    print(json.dumps(generate_scenarios(5), indent=2))
