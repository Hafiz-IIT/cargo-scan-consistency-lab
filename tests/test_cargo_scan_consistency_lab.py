import unittest

from cargo_scan_consistency_lab import CargoRecord, compare, review_required


class CargoConsistencyTests(unittest.TestCase):
    def test_matching_records_pass(self):
        record = CargoRecord("textiles", 1000, 100, 100, 100, True)
        self.assertEqual(compare(record, record), [])

    def test_weight_mismatch_detected(self):
        d = CargoRecord("textiles", 1000, 100, 100, 100, True)
        o = CargoRecord("textiles", 1200, 100, 100, 100, True)
        fields = {x.field for x in compare(d, o)}
        self.assertIn("weight_kg", fields)

    def test_nonpositive_physical_measurements_are_rejected(self):
        with self.assertRaises(ValueError):
            CargoRecord("textiles", 0, 100, 100, 100, True)
        with self.assertRaises(ValueError):
            CargoRecord("textiles", 1000, -1, 100, 100, True)

    def test_invalid_tolerance_is_rejected(self):
        record = CargoRecord("textiles", 1000, 100, 100, 100, True)
        with self.assertRaises(ValueError):
            compare(record, record, weight_tolerance_ratio=-0.1)

    def test_invalid_record_types_rejected(self):
        with self.assertRaises(TypeError):
            compare(None, None)

    def test_extreme_finite_measurements_do_not_crash_relative_comparison(self):
        declared = CargoRecord("textiles", 1e-308, 1e-308, 1e-308, 1e-308, True)
        observed = CargoRecord("textiles", 1e308, 1e308, 1e308, 1e308, True)
        discrepancies = compare(declared, observed)
        self.assertEqual({item.field for item in discrepancies}, {
            "weight_kg", "length_cm", "width_cm", "height_cm"
        })
        self.assertEqual(next(x for x in discrepancies if x.field == "weight_kg").severity, "high")

    def test_extremely_large_integer_measurement_is_rejected_cleanly(self):
        with self.assertRaises(ValueError):
            CargoRecord("textiles", 10 ** 10000, 1, 1, 1, True)

    def test_category_and_seal_trigger_review(self):
        d = CargoRecord("textiles", 1000, 100, 100, 100, True)
        o = CargoRecord("electronics", 1000, 100, 100, 100, False)
        discrepancies = compare(d, o)
        self.assertTrue(review_required(discrepancies))
        self.assertEqual({x.field for x in discrepancies}, {"category", "seal_intact"})


if __name__ == "__main__":
    unittest.main()
