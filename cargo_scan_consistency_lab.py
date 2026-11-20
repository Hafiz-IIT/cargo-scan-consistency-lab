from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class CargoRecord:
    category: str
    weight_kg: float
    length_cm: float
    width_cm: float
    height_cm: float
    seal_intact: bool

    def __post_init__(self) -> None:
        if not isinstance(self.category, str) or not self.category.strip():
            raise ValueError("category must be non-empty")
        for name in ("weight_kg", "length_cm", "width_cm", "height_cm"):
            value = getattr(self, name)
            if (isinstance(value, bool) or not isinstance(value, (int, float)) or
                    not isfinite(value) or value <= 0):
                raise ValueError(f"{name} must be finite and positive")
        if not isinstance(self.seal_intact, bool):
            raise ValueError("seal_intact must be boolean")


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
    for name, value in (("weight_tolerance_ratio", weight_tolerance_ratio),
                        ("dimension_tolerance_ratio", dimension_tolerance_ratio)):
        if (isinstance(value, bool) or not isinstance(value, (int, float)) or
                not isfinite(value) or not 0 <= value <= 1):
            raise ValueError(f"{name} must be finite and between 0 and 1")
    out: list[Discrepancy] = []

    if declared.category.strip().casefold() != observed.category.strip().casefold():
        out.append(Discrepancy("category", declared.category, observed.category, "high"))

    weight_ratio = abs(observed.weight_kg - declared.weight_kg) / max(1.0, declared.weight_kg)
    if weight_ratio > weight_tolerance_ratio:
        severity = "high" if weight_ratio > weight_tolerance_ratio * 2 else "medium"
        out.append(Discrepancy("weight_kg", declared.weight_kg, observed.weight_kg, severity))

    for field in ("length_cm", "width_cm", "height_cm"):
        d = float(getattr(declared, field))
        o = float(getattr(observed, field))
        ratio = abs(o - d) / max(1.0, d)
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
