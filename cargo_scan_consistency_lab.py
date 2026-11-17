from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class CargoRecord:
    category: str
    weight_kg: float
    length_cm: float
    width_cm: float
    height_cm: float
    seal_intact: bool

    def __post_init__(self):
        if not isinstance(self.category, str) or not self.category.strip():
            raise ValueError("cargo category is required")
        measurements = (self.weight_kg, self.length_cm, self.width_cm, self.height_cm)
        if any(not isinstance(value, (int, float)) or isinstance(value, bool)
               or not math.isfinite(value) or value <= 0 for value in measurements):
            raise ValueError("cargo weight and dimensions must be finite and positive")
        if not isinstance(self.seal_intact, bool):
            raise ValueError("seal_intact must be a boolean")


@dataclass(frozen=True)
class Discrepancy:
    field: str
    declared: object
    observed: object
    severity: str


def compare(
    declared: CargoRecord,
    observed: CargoRecord,
    *,
    weight_tolerance_ratio: float = 0.05,
    dimension_tolerance_ratio: float = 0.10,
) -> list[Discrepancy]:
    tolerances = (weight_tolerance_ratio, dimension_tolerance_ratio)
    if any(not isinstance(value, (int, float)) or isinstance(value, bool)
           or not math.isfinite(value) or not 0 <= value <= 1 for value in tolerances):
        raise ValueError("tolerance ratios must be finite and within [0, 1]")
    out: list[Discrepancy] = []

    if declared.category.strip().lower() != observed.category.strip().lower():
        out.append(Discrepancy("category", declared.category, observed.category, "high"))

    weight_ratio = abs(observed.weight_kg - declared.weight_kg) / declared.weight_kg
    if weight_ratio > weight_tolerance_ratio:
        severity = "high" if weight_ratio > weight_tolerance_ratio * 2 else "medium"
        out.append(Discrepancy("weight_kg", declared.weight_kg, observed.weight_kg, severity))

    for field in ("length_cm", "width_cm", "height_cm"):
        d = float(getattr(declared, field))
        o = float(getattr(observed, field))
        ratio = abs(o - d) / d
        if ratio > dimension_tolerance_ratio:
            out.append(Discrepancy(field, d, o, "medium"))

    if declared.seal_intact != observed.seal_intact:
        out.append(Discrepancy("seal_intact", declared.seal_intact, observed.seal_intact, "high"))

    return out


def review_required(discrepancies: list[Discrepancy]) -> bool:
    return bool(discrepancies)


if __name__ == "__main__":
    declared = CargoRecord("textiles", 1000, 120, 100, 100, True)
    observed = CargoRecord("textiles", 1120, 120, 100, 100, False)
    print(compare(declared, observed))
