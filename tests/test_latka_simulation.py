import json
import tempfile
import unittest
from pathlib import Path

from latka_simulation import DEFAULT_EXPERIMENTS, run_reproduction, simulate


class LotkaSimulationTest(unittest.TestCase):
    def test_simulate_generates_expected_number_of_points(self) -> None:
        experiment = DEFAULT_EXPERIMENTS[0]
        rows = simulate(experiment)
        expected = int(round(experiment.total_time / experiment.dt)) + 1
        self.assertEqual(len(rows), expected)

    def test_simulate_population_is_non_negative(self) -> None:
        experiment = DEFAULT_EXPERIMENTS[0]
        rows = simulate(experiment)
        self.assertTrue(all(row["prey"] >= 0.0 for row in rows))
        self.assertTrue(all(row["predator"] >= 0.0 for row in rows))

    def test_run_reproduction_outputs_csv_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            output_dir = Path(d)
            summary = run_reproduction(output_dir)

            self.assertEqual(set(summary.keys()), {e.name for e in DEFAULT_EXPERIMENTS})

            for experiment in DEFAULT_EXPERIMENTS:
                self.assertTrue((output_dir / f"{experiment.name}.csv").exists())

            summary_path = output_dir / "summary.json"
            self.assertTrue(summary_path.exists())
            data = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertIn("paper", data)
            self.assertEqual(set(data["results"].keys()), {e.name for e in DEFAULT_EXPERIMENTS})


if __name__ == "__main__":
    unittest.main()
