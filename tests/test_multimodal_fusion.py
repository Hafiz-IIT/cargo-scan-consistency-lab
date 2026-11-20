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

    def test_conflict_within_correlated_group_requires_review(self):
        result = fuse_category_observations([
            SensorObservation("camera-a", "textiles", 0.95, "shared-vision"),
            SensorObservation("camera-b", "machinery", 0.80, "shared-vision"),
            SensorObservation("weight", "textiles", 0.90, "physical"),
        ])
        self.assertTrue(result.requires_review)
        self.assertEqual(set(result.conflicting_categories), {"machinery", "textiles"})

    def test_conflicting_groups_are_exposed(self):
        result = fuse_category_observations([
            SensorObservation("cam-a", "textiles", 0.9, "shared"),
            SensorObservation("cam-b", "machinery", 0.8, "shared"),
            SensorObservation("weight", "textiles", 0.9, "physical"),
        ])
        self.assertEqual(result.conflicting_groups, ("shared",))

    def test_high_confidence_disagreement_between_independent_groups_requires_review(self):
        result = fuse_category_observations([
            SensorObservation("camera", "textiles", 0.99, "vision"),
            SensorObservation("weight", "machinery", 0.05, "physical"),
        ])
        self.assertTrue(result.requires_review)
        self.assertEqual(set(result.conflicting_categories), {"textiles", "machinery"})

    def test_zero_confidence_within_conflicting_group_fails_closed(self):
        result = fuse_category_observations([
            SensorObservation("cam-a", "textiles", 0.0, "shared"),
            SensorObservation("cam-b", "machinery", 0.0, "shared"),
        ])
        self.assertTrue(result.requires_review)
        self.assertIsNone(result.predicted_category)
        self.assertEqual(result.conflicting_groups, ("shared",))

    def test_invalid_observation_collection_rejected(self):
        with self.assertRaises(ValueError):
            fuse_category_observations(None)

    def test_invalid_confidence_and_threshold_are_rejected(self):
        with self.assertRaises(ValueError):
            SensorObservation("camera", "textiles", 1.2, "vision")
        with self.assertRaises(ValueError):
            fuse_category_observations([], min_support=1.1)

    def test_extreme_numeric_confidence_and_support_threshold_fail_cleanly(self):
        huge = 10 ** 10000
        with self.assertRaises(ValueError):
            SensorObservation("camera", "textiles", huge, "vision")
        with self.assertRaises(ValueError):
            fuse_category_observations([], min_support=huge)
        with self.assertRaises(ValueError):
            generate_scenarios(10, anomaly_rate=huge)

    def test_conflict_requires_review(self):
        result = fuse_category_observations([
            SensorObservation("physical", "textiles", 0.80, "physical"),
            SensorObservation("visual", "machinery", 0.80, "vision"),
        ])
        self.assertTrue(result.requires_review)
        self.assertEqual(set(result.conflicting_categories), {"machinery", "textiles"})

    def test_scenario_generator_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            generate_scenarios(True)
        with self.assertRaises(ValueError):
            generate_scenarios(10, anomaly_rate=float("nan"))
        with self.assertRaises(ValueError):
            generate_scenarios(10, seed=True)

    def test_synthetic_scenarios_reproducible(self):
        a = generate_scenarios(10, seed=42)
        b = generate_scenarios(10, seed=42)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
