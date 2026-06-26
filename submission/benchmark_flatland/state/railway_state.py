"""Planner-friendly Flatland world state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AgentStateSummary:
    """Compact train state used by high-level policy selection."""

    handle: int
    state: str
    position: tuple[int, int] | None
    direction: int | None
    initial_position: tuple[int, int] | None
    target: tuple[int, int] | None
    speed: float | None
    waypoint_count: int


@dataclass(frozen=True)
class FlatlandWorldState:
    """Structured state analogous to WorldState in the embodied stack."""

    num_agents: int
    width: int
    height: int
    elapsed_steps: int
    max_episode_steps: int | None
    agents: tuple[AgentStateSummary, ...]
    malfunction_rate: float | None = None
    unique_initial_positions: int = 0
    unique_targets: int = 0
    min_waypoint_count: int = 0
    max_waypoint_count: int = 0
    mean_waypoint_count: float = 0.0
    raw_env_ref: Any | None = None

    @property
    def density(self) -> float:
        cells = max(self.width * self.height, 1)
        return self.num_agents / cells
