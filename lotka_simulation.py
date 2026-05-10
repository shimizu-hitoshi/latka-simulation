from __future__ import annotations

import argparse
import csv
import json
import random
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


@dataclass(frozen=True)
class Experiment:
    name: str
    description: str
    alpha: float
    num_papers: int
    seed: int


DEFAULT_EXPERIMENTS: List[Experiment] = [
    Experiment(
        name="baseline",
        description="Gilbert (1997) に基づく基本ケース",
        alpha=0.35,
        num_papers=1_000,
        seed=7,
    ),
    Experiment(
        name="higher_alpha",
        description="新規著者の流入を増やした感度分析",
        alpha=0.50,
        num_papers=1_000,
        seed=7,
    ),
    Experiment(
        name="larger_corpus",
        description="論文数を増やした感度分析",
        alpha=0.35,
        num_papers=5_000,
        seed=11,
    ),
]


def simulate(experiment: Experiment) -> List[Dict[str, int]]:
    rng = random.Random(experiment.seed)
    papers_per_author: List[int] = []
    paper_authors: List[int] = []

    for paper_id in range(1, experiment.num_papers + 1):
        assign_new_author = paper_id == 1 or rng.random() < experiment.alpha

        if assign_new_author:
            author_id = len(papers_per_author)
            papers_per_author.append(0)
        else:
            cited_paper_index = rng.randrange(len(paper_authors))
            author_id = paper_authors[cited_paper_index]

        papers_per_author[author_id] += 1
        paper_authors.append(author_id)

    distribution = Counter(papers_per_author)
    rows = [
        {
            "papers": papers,
            "authors": distribution[papers],
            "share": distribution[papers] / len(papers_per_author),
        }
        for papers in sorted(distribution)
    ]
    return rows


def run_reproduction(output_dir: Path) -> Dict[str, Dict[str, float]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    summary: Dict[str, Dict[str, float]] = {}

    for experiment in DEFAULT_EXPERIMENTS:
        rows = simulate(experiment)
        csv_path = output_dir / f"{experiment.name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.DictWriter(fp, fieldnames=["papers", "authors", "share"])
            writer.writeheader()
            writer.writerows(rows)

        total_authors = sum(int(row["authors"]) for row in rows)
        total_papers = sum(int(row["papers"]) * int(row["authors"]) for row in rows)
        summary[experiment.name] = {
            "alpha": experiment.alpha,
            "num_papers": experiment.num_papers,
            "num_authors": total_authors,
            "mean_papers_per_author": total_papers / total_authors,
            "max_papers_per_author": max(int(row["papers"]) for row in rows),
        }

    summary_path = output_dir / "summary.json"
    with summary_path.open("w", encoding="utf-8") as fp:
        json.dump(
            {
                "paper": "https://journals.sagepub.com/doi/10.5153/sro.85",
                "model": "Lotka's Law",
                "rule": "Each new paper is assigned to a new author with probability alpha, otherwise to the author of a randomly selected existing paper.",
                "experiments": [asdict(e) for e in DEFAULT_EXPERIMENTS],
                "results": summary,
            },
            fp,
            ensure_ascii=False,
            indent=2,
        )

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Lotka's Law 論文再現実験を実行します")
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="実験結果CSVとsummary.jsonの出力先ディレクトリ (default: outputs)",
    )
    args = parser.parse_args()

    summary = run_reproduction(Path(args.output_dir))
    print("Reproduction experiments completed.")
    for name, values in summary.items():
        print(
            f"- {name}: authors={values['num_authors']:.0f}, "
            f"mean_papers_per_author={values['mean_papers_per_author']:.4f}, "
            f"max_papers_per_author={values['max_papers_per_author']:.0f}"
        )


if __name__ == "__main__":
    main()
