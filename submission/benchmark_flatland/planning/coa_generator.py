"""Deterministic COA generation for Flatland policy families."""

from __future__ import annotations

from benchmark_flatland.planning.candidate_coa import CandidateCOA
from benchmark_flatland.state.railway_state import FlatlandWorldState


def generate_flatland_coas(state: FlatlandWorldState) -> list[CandidateCOA]:
    """Generate policy-family candidates for the current railway scenario."""

    dense = state.num_agents >= 25
    return [
        CandidateCOA(
            name="entering_prevention",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLAEnteringPreventionPolicy"
            ),
            rationale=(
                "Preserve deadlock avoidance while preventing conflicting "
                "simultaneous map entry."
            ),
            expected_strengths=("small_and_medium_scenarios", "entry_conflicts"),
            risk_notes=("can remain too conservative in dense cases",),
            metadata={"preferred_when": "num_agents < 25", "dense": dense},
        ),
        CandidateCOA(
            name="less_conservative_dense",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLALessConservativePolicy"
            ),
            rationale=(
                "Relax spacing and switch penalties when dense scenarios "
                "otherwise over-block trains."
            ),
            expected_strengths=("dense_scenarios", "overblocking_reduction"),
            risk_notes=("can regress already-solved sparse scenarios",),
            metadata={"preferred_when": "num_agents >= 25", "dense": dense},
        ),
        CandidateCOA(
            name="fast_no_spacing_scene4_dense",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLAFastNoSpacingPolicy"
            ),
            rationale=(
                "Remove spacing and switch penalties for the measured dense "
                "scene-4 low-waypoint pattern where conservative buffering "
                "over-blocked flow."
            ),
            expected_strengths=("dense_scene4_low_waypoint", "overblocking_reduction"),
            risk_notes=("high collision/deadlock risk outside the measured pattern",),
            metadata={
                "preferred_when": "25 agents, 2 waypoints, 16 targets, 15 starts",
                "dense": dense,
            },
        ),
        CandidateCOA(
            name="fast_switch_scene5_dense",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLAFastSwitchPolicy"
            ),
            rationale=(
                "Allow zero-spacing movement while retaining switch and "
                "oncoming-train accounting for the measured dense scene-5 "
                "low-waypoint pattern."
            ),
            expected_strengths=("dense_scene5_low_waypoint", "throughput_with_switch_guard"),
            risk_notes=("regressed broader dense schedules in focused sweeps",),
            metadata={
                "preferred_when": "25 agents, 2 waypoints, 19 targets, 18 starts",
                "dense": dense,
            },
        ),
        CandidateCOA(
            name="drop_blocked_bottleneck",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLADropBlockedPolicy"
            ),
            rationale=(
                "Drop the next intermediate stop after sustained blocking in "
                "low-diversity bottleneck schedules."
            ),
            expected_strengths=("bottleneck_schedules", "blocked_intermediate_recovery"),
            risk_notes=("can regress broader scene-4/scene-5 schedules",),
            metadata={
                "preferred_when": "low waypoint and target diversity bottleneck",
                "dense": dense,
            },
        ),
        CandidateCOA(
            name="conservative_dense_flow",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLAConservativePolicy"
            ),
            rationale=(
                "Increase spacing when dense low-waypoint flow suffers from "
                "switch contention."
            ),
            expected_strengths=("dense_low_waypoint_scene4_scene5", "collision_buffering"),
            risk_notes=("can over-block sparse or long-waypoint schedules",),
            metadata={
                "preferred_when": "dense low-waypoint high target diversity",
                "dense": dense,
            },
        ),
        CandidateCOA(
            name="alternative_two_scene4",
            policy_class_path=(
                "benchmark_flatland.policy.deadlock_portfolio_policy."
                "DLAAlternativeTwoPolicy"
            ),
            rationale=(
                "Try limited alternative routing at the first intermediate "
                "when a medium scene-4 style schedule benefits from rerouting."
            ),
            expected_strengths=("medium_scene4_low_waypoint", "limited_rerouting"),
            risk_notes=("can fail or severely regress broader long-waypoint schedules",),
            metadata={
                "preferred_when": "10 agents, 2 waypoints, 9 unique targets",
                "dense": dense,
            },
        ),
    ]
