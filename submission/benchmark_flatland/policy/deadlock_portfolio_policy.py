"""Small policy variants built on the maintained Flatland deadlock baseline.

These classes keep the official ``RailEnvPolicy`` interface and only tune
parameters exposed by the maintained baseline. They are intentionally simple:
we use them to establish measured gains before adding heavier reservation
planning.
"""

from __future__ import annotations

from flatland_baselines.deadlock_avoidance_heuristic.policy.deadlock_avoidance_policy import (
    DeadLockAvoidancePolicy,
)


class DLAConservativePolicy(DeadLockAvoidancePolicy):
    """Slightly more conservative than the default baseline."""

    def __init__(self):
        super().__init__(
            min_free_cell=2,
            count_num_opp_agents_towards_min_free_cell=True,
            use_switches_heuristic=True,
            use_entering_prevention=True,
            seed=42,
        )


class DLALessConservativePolicy(DeadLockAvoidancePolicy):
    """Allow trains to move with less extra spacing than the default policy."""

    def __init__(self):
        super().__init__(
            min_free_cell=1,
            count_num_opp_agents_towards_min_free_cell=False,
            use_switches_heuristic=False,
            use_entering_prevention=False,
            seed=42,
        )


class DLAFastNoSpacingPolicy(DeadLockAvoidancePolicy):
    """Aggressive flow policy for the measured dense scene-4 low-waypoint case."""

    def __init__(self):
        super().__init__(
            min_free_cell=0,
            count_num_opp_agents_towards_min_free_cell=False,
            use_switches_heuristic=False,
            use_entering_prevention=False,
            seed=42,
        )


class DLAFastSwitchPolicy(DeadLockAvoidancePolicy):
    """Aggressive flow policy that keeps switch/oncoming accounting enabled."""

    def __init__(self):
        super().__init__(
            min_free_cell=0,
            count_num_opp_agents_towards_min_free_cell=True,
            use_switches_heuristic=True,
            use_entering_prevention=False,
            seed=42,
        )


class DLAEnteringPreventionPolicy(DeadLockAvoidancePolicy):
    """Default deadlock logic plus prevention of simultaneous map entry."""

    def __init__(self):
        super().__init__(
            min_free_cell=1,
            count_num_opp_agents_towards_min_free_cell=True,
            use_switches_heuristic=True,
            use_entering_prevention=True,
            seed=42,
        )


class DLADropBlockedPolicy(DeadLockAvoidancePolicy):
    """Default deadlock logic with intermediate-stop dropping after blocking."""

    def __init__(self):
        super().__init__(
            min_free_cell=1,
            count_num_opp_agents_towards_min_free_cell=True,
            use_switches_heuristic=True,
            use_entering_prevention=False,
            drop_next_threshold=20,
            k_shortest_path_cutoff=450,
            seed=42,
        )


class DLAAlternativeTwoPolicy(DeadLockAvoidancePolicy):
    """Try two alternatives at the first remaining intermediate when blocked."""

    def __init__(self):
        super().__init__(
            min_free_cell=1,
            count_num_opp_agents_towards_min_free_cell=False,
            use_switches_heuristic=False,
            use_entering_prevention=True,
            use_alternative_at_first_intermediate_and_then_always_first_strategy=2,
            drop_next_threshold=20,
            k_shortest_path_cutoff=450,
            seed=42,
        )


class AdaptiveDLA25LessElseEnteringPolicy:
    """Adaptive portfolio selected from measured Flatland source-mode results.

    Rationale from the 27-scenario starter-kit curriculum:
    - Dense 25-agent cases benefited from less-conservative movement.
    - 1-agent and 10-agent cases were safer with entering-prevention enabled.

    The policy chooses once from observable environment metadata and then
    delegates every action to the selected official-interface policy.
    """

    def __init__(self):
        from benchmark_flatland.policy.flatland_decision_policy import (
            FlatlandDecisionPolicy,
        )

        self._decision_policy = FlatlandDecisionPolicy()

    def act_many(self, handles, observations, **kwargs):
        return self._decision_policy.act_many(handles, observations, **kwargs)

    def act(self, handle, observation, **kwargs):
        return self._decision_policy.act(handle, observation, **kwargs)

    def reset(self, *args, **kwargs):
        return self._decision_policy.reset(*args, **kwargs)

    @property
    def selected_policy_name(self):
        return self._decision_policy.selected_coa

    @property
    def selection_trace(self):
        return self._decision_policy.selection_trace
