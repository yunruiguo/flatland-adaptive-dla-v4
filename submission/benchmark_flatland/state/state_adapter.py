"""Convert a Flatland RailEnv into a planner-friendly state summary."""

from __future__ import annotations

from fractions import Fraction
from statistics import mean
from typing import Any

from benchmark_flatland.state.railway_state import AgentStateSummary, FlatlandWorldState


def _tuple_or_none(value: Any) -> tuple[int, int] | None:
    if value is None:
        return None
    return tuple(value)


def _speed_to_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, Fraction):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_world_state(env: Any, keep_raw_env_ref: bool = False) -> FlatlandWorldState:
    """Extract the minimal state needed by the Flatland decision pipeline."""

    agents = []
    for agent in getattr(env, "agents", []):
        speed = None
        speed_counter = getattr(agent, "speed_counter", None)
        if speed_counter is not None:
            speed = _speed_to_float(getattr(speed_counter, "speed", None))
        agents.append(
            AgentStateSummary(
                handle=int(getattr(agent, "handle", len(agents))),
                state=str(getattr(agent, "state", "unknown")),
                position=_tuple_or_none(getattr(agent, "position", None)),
                direction=getattr(agent, "direction", None),
                initial_position=_tuple_or_none(getattr(agent, "initial_position", None)),
                target=_tuple_or_none(getattr(agent, "target", None)),
                speed=speed,
                waypoint_count=len(getattr(agent, "waypoints", []) or []),
            )
        )

    malfunction_rate = None
    malfunction_data = getattr(env, "malfunction_process_data", None)
    if malfunction_data is not None:
        malfunction_rate = getattr(malfunction_data, "malfunction_rate", None)

    initial_positions = {
        agent.initial_position for agent in agents if agent.initial_position is not None
    }
    targets = {agent.target for agent in agents if agent.target is not None}
    waypoint_counts = [agent.waypoint_count for agent in agents]

    return FlatlandWorldState(
        num_agents=int(env.get_num_agents()),
        width=int(getattr(env, "width")),
        height=int(getattr(env, "height")),
        elapsed_steps=int(getattr(env, "_elapsed_steps", 0)),
        max_episode_steps=getattr(env, "_max_episode_steps", None),
        agents=tuple(agents),
        malfunction_rate=malfunction_rate,
        unique_initial_positions=len(initial_positions),
        unique_targets=len(targets),
        min_waypoint_count=min(waypoint_counts) if waypoint_counts else 0,
        max_waypoint_count=max(waypoint_counts) if waypoint_counts else 0,
        mean_waypoint_count=float(mean(waypoint_counts)) if waypoint_counts else 0.0,
        raw_env_ref=env if keep_raw_env_ref else None,
    )
