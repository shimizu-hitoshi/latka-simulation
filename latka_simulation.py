from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class LotkaVolterraParameters:
    alpha: float
    beta: float
    delta: float
    gamma: float


@dataclass(frozen=True)
class Experiment:
    name: str
    description: str
    parameters: LotkaVolterraParameters
    prey0: float
    predator0: float
    total_time: float
    dt: float


DEFAULT_EXPERIMENTS: List[Experiment] = [
    Experiment(
        name="baseline",
        description="論文再現用の基本ケース",
        parameters=LotkaVolterraParameters(alpha=1.1, beta=0.4, delta=0.1, gamma=0.4),
        prey0=40.0,
        predator0=9.0,
        total_time=30.0,
        dt=0.05,
    ),
    Experiment(
        name="high_initial_prey",
        description="初期被食者数を増やした感度分析",
        parameters=LotkaVolterraParameters(alpha=1.1, beta=0.4, delta=0.1, gamma=0.4),
        prey0=60.0,
        predator0=9.0,
        total_time=30.0,
        dt=0.05,
    ),
    Experiment(
        name="low_initial_predator",
        description="初期捕食者数を減らした感度分析",
        parameters=LotkaVolterraParameters(alpha=1.1, beta=0.4, delta=0.1, gamma=0.4),
        prey0=40.0,
        predator0=5.0,
        total_time=30.0,
        dt=0.05,
    ),
]


def _derivatives(prey: float, predator: float, p: LotkaVolterraParameters) -> tuple[float, float]:
    dprey = p.alpha * prey - p.beta * prey * predator
    dpredator = p.delta * prey * predator - p.gamma * predator
    return dprey, dpredator


def simulate(experiment: Experiment) -> List[Dict[str, float]]:
    prey = float(experiment.prey0)
    predator = float(experiment.predator0)
    t = 0.0
    result: List[Dict[str, float]] = [{"t": t, "prey": prey, "predator": predator}]

    steps = int(round(experiment.total_time / experiment.dt))
    dt = experiment.dt

    for step in range(1, steps + 1):
        k1x, k1y = _derivatives(prey, predator, experiment.parameters)

        k2x, k2y = _derivatives(prey + (dt * k1x) / 2.0, predator + (dt * k1y) / 2.0, experiment.parameters)
        k3x, k3y = _derivatives(prey + (dt * k2x) / 2.0, predator + (dt * k2y) / 2.0, experiment.parameters)
        k4x, k4y = _derivatives(prey + dt * k3x, predator + dt * k3y, experiment.parameters)

        prey += (dt / 6.0) * (k1x + 2.0 * k2x + 2.0 * k3x + k4x)
        predator += (dt / 6.0) * (k1y + 2.0 * k2y + 2.0 * k3y + k4y)

        prey = max(prey, 0.0)
        predator = max(predator, 0.0)
        t = round(step * dt, 10)
        result.append({"t": t, "prey": prey, "predator": predator})

    return result


def run_reproduction(output_dir: Path) -> Dict[str, Dict[str, float]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary: Dict[str, Dict[str, float]] = {}

    for experiment in DEFAULT_EXPERIMENTS:
        rows = simulate(experiment)
        csv_path = output_dir / f"{experiment.name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=["t", "prey", "predator"])
            writer.writeheader()
            writer.writerows(rows)

        summary[experiment.name] = {
            "max_prey": max(row["prey"] for row in rows),
            "max_predator": max(row["predator"] for row in rows),
            "final_prey": rows[-1]["prey"],
            "final_predator": rows[-1]["predator"],
            "dt": experiment.dt,
            "total_time": experiment.total_time,
        }

    summary_path = output_dir / "summary.json"
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(
            {
                "paper": "https://journals.sagepub.com/doi/10.5153/sro.85",
                "model": "Lotka-Volterra",
                "experiments": [
                    {
                        "name": e.name,
                        "description": e.description,
                        "parameters": asdict(e.parameters),
                        "prey0": e.prey0,
                        "predator0": e.predator0,
                        "total_time": e.total_time,
                        "dt": e.dt,
                    }
                    for e in DEFAULT_EXPERIMENTS
                ],
                "results": summary,
            },
            fp,
            ensure_ascii=False,
            indent=2,
        )

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Lotka-Volterra論文再現実験を実行します")
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="実験結果CSVとsummary.jsonの出力先ディレクトリ (default: outputs)",
    )
    args = parser.parse_args()

    summary = run_reproduction(Path(args.output_dir))
    print("Reproduction experiments completed.")
    for name, values in summary.items():
        print(f"- {name}: final_prey={values['final_prey']:.4f}, final_predator={values['final_predator']:.4f}")


if __name__ == "__main__":
    main()
