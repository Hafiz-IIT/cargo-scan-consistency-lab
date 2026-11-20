from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from math import isfinite


@dataclass(frozen=True)
class SensorObservation:
    channel: str
    observed_category: str
    confidence: float
    independent_group: str

    def __post_init__(self) -> None:
        for name, value in (("channel", self.channel), ("observed_category", self.observed_category),
                            ("independent_group", self.independent_group)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be non-empty")
        if (isinstance(self.confidence, bool) or not isinstance(self.confidence, (int, float)) or
                not isfinite(self.confidence) or not 0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be finite and between 0 and 1")

    def normalized_confidence(self) -> float:
        return float(self.confidence)


@dataclass(frozen=True)
class FusionResult:
    predicted_category: str | None
    support: float
    independent_groups: int
    conflicting_categories: tuple[str, ...]
    requires_review: bool
    conflicting_groups: tuple[str, ...] = ()


def fuse_category_observations(
    observations: list[SensorObservation],
    *,
    min_independent_groups: int = 2,
    min_support: float = 0.75,
) -> FusionResult:
    """Fuse categorical evidence without double-counting correlated channels.

    For each independent group, only the strongest observation for a category is
    retained. The function is intentionally transparent and does not represent
    a calibrated physical sensor model.
    """
    if isinstance(min_independent_groups, bool) or not isinstance(min_independent_groups, int) or min_independent_groups < 1:
        raise ValueError("min_independent_groups must be a positive integer")
    if (isinstance(min_support, bool) or not isinstance(min_support, (int, float)) or
            not isfinite(min_support) or not 0.0 <= min_support <= 1.0):
        raise ValueError("min_support must be finite and between 0 and 1")
    if not isinstance(observations, list) or any(not isinstance(obs, SensorObservation) for obs in observations):
        raise ValueError("observations must be a list of SensorObservation values")
    if not observations:
        return FusionResult(None, 0.0, 0, (), True, ())

    best_by_group: dict[str, SensorObservation] = {}
    categories_by_group: dict[str, set[str]] = defaultdict(set)
    for obs in observations:
        categories_by_group[obs.independent_group].add(obs.observed_category.strip().casefold())
        current = best_by_group.get(obs.independent_group)
        if current is None or obs.normalized_confidence() > current.normalized_confidence():
            best_by_group[obs.independent_group] = obs

    scores: dict[str, float] = defaultdict(float)
    for obs in best_by_group.values():
        scores[obs.observed_category.strip().casefold()] += obs.normalized_confidence()

    total = sum(scores.values())
    if total <= 0:
        return FusionResult(None, 0.0, len(best_by_group), tuple(sorted(scores)), True, conflicting_groups)

    predicted, raw = max(scores.items(), key=lambda kv: (kv[1], kv[0]))
    support = raw / total
    conflicting_groups = tuple(sorted(
        group for group, categories in categories_by_group.items() if len(categories) > 1
    ))
    all_categories = set(scores)
    for group in conflicting_groups:
        all_categories.update(categories_by_group[group])
    conflicts = tuple(sorted(all_categories)) if len(all_categories) > 1 else ()

    requires_review = (
        len(best_by_group) < min_independent_groups
        or support < min_support
        or bool(conflicts and support < 0.90)
        or bool(conflicting_groups)
    )
    return FusionResult(
        predicted_category=predicted,
        support=round(support, 6),
        independent_groups=len(best_by_group),
        conflicting_categories=conflicts,
        requires_review=requires_review,
        conflicting_groups=conflicting_groups,
    )


def declaration_consistent(
    declared_category: str,
    fusion: FusionResult,
) -> bool:
    if not isinstance(declared_category, str) or not declared_category.strip():
        raise ValueError("declared_category must be a non-empty string")
    if not isinstance(fusion, FusionResult):
        raise TypeError("fusion must be a FusionResult")
    return (
        fusion.predicted_category is not None
        and fusion.predicted_category == declared_category.strip().casefold()
        and not fusion.requires_review
    )


if __name__ == "__main__":
    sample = [
        SensorObservation("weight-profile", "textiles", 0.90, "physical"),
        SensorObservation("visual-classifier", "textiles", 0.85, "vision"),
    ]
    print(fuse_category_observations(sample))
