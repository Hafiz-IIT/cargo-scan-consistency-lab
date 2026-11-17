from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
import math


@dataclass(frozen=True)
class SensorObservation:
    channel: str
    observed_category: str
    confidence: float
    independent_group: str

    def __post_init__(self):
        if any(not isinstance(value, str) or not value.strip()
               for value in (self.channel, self.observed_category, self.independent_group)):
            raise ValueError("sensor channel, category and independence group are required")
        if not isinstance(self.confidence, (int, float)) or isinstance(self.confidence, bool) or not math.isfinite(self.confidence) or not 0 <= self.confidence <= 1:
            raise ValueError("sensor confidence must be finite and within [0, 1]")

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
    if not isinstance(min_independent_groups, int) or isinstance(min_independent_groups, bool) or min_independent_groups < 1:
        raise ValueError("min_independent_groups must be a positive integer")
    if not isinstance(min_support, (int, float)) or isinstance(min_support, bool) or not math.isfinite(min_support) or not 0 <= min_support <= 1:
        raise ValueError("min_support must be finite and within [0, 1]")
    if not observations:
        return FusionResult(None, 0.0, 0, (), True)

    best_by_group: dict[str, SensorObservation] = {}
    categories_by_group: dict[str, set[str]] = defaultdict(set)
    for obs in observations:
        categories_by_group[obs.independent_group].add(obs.observed_category.strip().lower())
        current = best_by_group.get(obs.independent_group)
        if current is None or obs.normalized_confidence() > current.normalized_confidence():
            best_by_group[obs.independent_group] = obs

    conflicting_groups = tuple(sorted(
        group for group, categories in categories_by_group.items() if len(categories) > 1
    ))
    scores: dict[str, float] = defaultdict(float)
    for obs in best_by_group.values():
        scores[obs.observed_category.strip().lower()] += obs.normalized_confidence()

    total = sum(scores.values())
    if total <= 0:
        return FusionResult(None, 0.0, len(best_by_group), tuple(sorted(scores)), True, conflicting_groups)

    predicted, raw = max(scores.items(), key=lambda kv: (kv[1], kv[0]))
    support = raw / total
    conflicts = tuple(sorted(scores)) if len(scores) > 1 else ()

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
    return (
        fusion.predicted_category is not None
        and fusion.predicted_category == declared_category.strip().lower()
        and not fusion.requires_review
    )


if __name__ == "__main__":
    sample = [
        SensorObservation("weight-profile", "textiles", 0.90, "physical"),
        SensorObservation("visual-classifier", "textiles", 0.85, "vision"),
    ]
    print(fuse_category_observations(sample))
