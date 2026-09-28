import unittest

from multimodal_fusion import (
    SensorObservation,
    declaration_consistent,
    fuse_category_observations,
)
from synthetic_scenarios import generate_scenarios


class MultimodalFusionTests(unittest.TestCase):
    def test_independent_agreement_can_clear_review(self):
        result = fuse_category_observations([
            SensorObservation("weight-profile", "textiles", 0.95, "physical"),
            SensorObservation("visual", "textiles", 0.90, "vision"),
        ])
        self.assertEqual(result.predicted_category, "textiles")
        self.assertFalse(result.requires_review)
        self.assertTrue(declaration_consistent("Textiles", result))

    def test_correlated_channels_count_once(self):
        result = fuse_category_observations([
            SensorObservation("camera-a", "electronics", 0.95, "vision"),
            SensorObservation("camera-b", "electronics", 0.90, "vision"),
        ])
        self.assertEqual(result.independent_groups, 1)
        self.assertTrue(result.requires_review)

    def test_conflict_requires_review(self):
        result = fuse_category_observations([
            SensorObservation("physical", "textiles", 0.80, "physical"),
            SensorObservation("visual", "machinery", 0.80, "vision"),
        ])
        self.assertTrue(result.requires_review)
        self.assertEqual(set(result.conflicting_categories), {"machinery", "textiles"})

    def test_synthetic_scenarios_reproducible(self):
        a = generate_scenarios(10, seed=42)
        b = generate_scenarios(10, seed=42)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
