"""Collect Flatland trajectory-analysis outputs into compact summaries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import pandas as pd


def collect_analysis_dirs(root: Path) -> list[Path]:
    """Return analysis directories that contain ``all_trains_arrived.csv``."""

    return sorted(
        path
        for path in root.glob("*_analysis")
        if (path / "all_trains_arrived.csv").exists()
    )


def summarize_analysis_dirs(
    analysis_dirs: Iterable[Path],
    baseline: str,
    output_dir: Path,
) -> pd.DataFrame:
    """Write CSV/JSON summaries for a set of Flatland analysis directories."""

    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for analysis_dir in analysis_dirs:
        arrived = pd.read_csv(analysis_dir / "all_trains_arrived.csv").iloc[-1]
        env = pd.read_csv(analysis_dir / "env_stats.csv").iloc[0]
        scenario = analysis_dir.name.removesuffix("_analysis")
        rows.append(
            {
                "baseline": baseline,
                "scenario": scenario,
                "episode_id": arrived["episode_id"],
                "env_time": int(arrived["env_time"]),
                "success_rate": float(arrived["success_rate"]),
                "normalized_reward": float(arrived["normalized_reward"]),
                "num_agents": int(env["num_agents"]),
                "max_episode_steps": int(env["max_episode_steps"]),
                "analysis_dir": str(analysis_dir),
            }
        )

    df = pd.DataFrame(rows).sort_values("scenario")
    df.to_csv(output_dir / "results.csv", index=False)
    summary = {
        "baseline": baseline,
        "num_scenarios": int(len(df)),
        "mean_success_rate": float(df["success_rate"].mean()) if len(df) else None,
        "mean_normalized_reward": float(df["normalized_reward"].mean())
        if len(df)
        else None,
        "sum_normalized_reward": float(df["normalized_reward"].sum())
        if len(df)
        else None,
        "min_success_rate": float(df["success_rate"].min()) if len(df) else None,
        "max_success_rate": float(df["success_rate"].max()) if len(df) else None,
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    return df

