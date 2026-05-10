import json
import tempfile
import unittest
from pathlib import Path

from lotka_simulation import DEFAULT_EXPERIMENTS, run_reproduction, simulate


class LotkaSimulationTest(unittest.TestCase):
    def test_simulate_generates_distribution_covering_all_authors(self) -> None:
        experiment = DEFAULT_EXPERIMENTS[0]
        rows = simulate(experiment)
        total_authors = sum(row["authors"] for row in rows)
        self.assertGreater(total_authors, 0)
        self.assertEqual(total_authors, run_reproduction(Path(tempfile.gettempdir()))[experiment.name]["num_authors"])

    def test_simulate_distribution_is_valid(self) -> None:
        experiment = DEFAULT_EXPERIMENTS[0]
        rows = simulate(experiment)
        self.assertTrue(all(row["papers"] >= 1 for row in rows))
        self.assertTrue(all(row["authors"] >= 1 for row in rows))
        self.assertTrue(all(0.0 < row["share"] <= 1.0 for row in rows))
        self.assertEqual(rows, sorted(rows, key=lambda row: row["papers"]))

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
            self.assertEqual(data["model"], "Lotka's Law")
            self.assertIn("rule", data)
            self.assertEqual(set(data["results"].keys()), {e.name for e in DEFAULT_EXPERIMENTS})


if __name__ == "__main__":
    unittest.main()
