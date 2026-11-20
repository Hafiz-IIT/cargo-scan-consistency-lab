from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _finite_float(name: str, value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    try:
        normalized = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not isfinite(normalized):
        raise ValueError(f"{name} must be a finite number")
    return normalized


def _relative_ratio(difference: float, baseline: float) -> float:
    try:
        return difference / baseline
    except OverflowError:
        return float("inf")


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
            value = _finite_float(name, getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be finite and positive")
            object.__setattr__(self, name, value)
        if not isinstance(self.seal_intact, bool):
            raise ValueError("seal_intact must be boolean")


@dataclass(frozen=True)
class Discrepancy:
    field: str
    declared: object
    observed: object
    severity: str

    def __post_init__(self):
        if not isinstance(self.field, str) or not self.field.strip():
            raise ValueError("discrepancy field must be non-empty")
        if not isinstance(self.severity, str) or self.severity not in {"low", "medium", "high"}:
            raise ValueError("severity must be low, medium or high")


def compare(
    declared: CargoRecord,
    observed: CargoRecord,
    *,
    weight_tolerance_ratio: float = 0.05,
    dimension_tolerance_ratio: float = 0.10,
) -> list[Discrepancy]:
    if not isinstance(declared, CargoRecord) or not isinstance(observed, CargoRecord):
        raise TypeError("declared and observed must be CargoRecord values")
    weight_tolerance_ratio = _finite_float("weight_tolerance_ratio", weight_tolerance_ratio)
    dimension_tolerance_ratio = _finite_float("dimension_tolerance_ratio", dimension_tolerance_ratio)
    if not 0 <= weight_tolerance_ratio <= 1:
        raise ValueError("weight_tolerance_ratio must be between 0 and 1")
    if not 0 <= dimension_tolerance_ratio <= 1:
        raise ValueError("dimension_tolerance_ratio must be between 0 and 1")
    out: list[Discrepancy] = []

    if declared.category.strip().casefold() != observed.category.strip().casefold():
        out.append(Discrepancy("category", declared.category, observed.category, "high"))

    weight_difference = abs(observed.weight_kg - declared.weight_kg)
    weight_ratio = _relative_ratio(weight_difference, declared.weight_kg)
    if weight_ratio > weight_tolerance_ratio:
        severity = "high" if weight_ratio > weight_tolerance_ratio * 2 else "medium"
        out.append(Discrepancy("weight_kg", declared.weight_kg, observed.weight_kg, severity))

    for field in ("length_cm", "width_cm", "height_cm"):
        d = float(getattr(declared, field))
        o = float(getattr(observed, field))
        ratio = _relative_ratio(abs(o - d), d)
        if ratio > dimension_tolerance_ratio:
            out.append(Discrepancy(field, d, o, "medium"))

    if declared.seal_intact != observed.seal_intact:
        out.append(Discrepancy("seal_intact", declared.seal_intact, observed.seal_intact, "high"))

    return out


def review_required(discrepancies: list[Discrepancy]) -> bool:
    if not isinstance(discrepancies, list) or any(not isinstance(item, Discrepancy) for item in discrepancies):
        raise ValueError("discrepancies must be a list of Discrepancy values")
    return bool(discrepancies)


if __name__ == "__main__":
    declared = CargoRecord("textiles", 1000, 120, 100, 100, True)
    observed = CargoRecord("textiles", 1120, 120, 100, 100, False)
    print(compare(declared, observed))
