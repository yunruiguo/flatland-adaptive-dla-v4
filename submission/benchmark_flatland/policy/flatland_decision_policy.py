"""Official-interface Flatland policy backed by the Decision Pipeline."""

from __future__ import annotations

import importlib

from benchmark_flatland.planning.policy_selector import select_best_coa
from benchmark_flatland.state.state_adapter import extract_world_state


def _load_policy_class(path: str):
    module_name, _, class_name = path.rpartition(".")
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


class FlatlandDecisionPolicy:
    """RailEnvPolicy-compatible wrapper around the Flatland Decision Pipeline."""

    def __init__(self):
        self._policy = None
        self.selected_coa = None
        self.selection_trace = []

    def _ensure_policy(self, env):
        if self._policy is not None:
            return
        state = extract_world_state(env)
        selected = select_best_coa(state)
        policy_cls = _load_policy_class(selected.coa.policy_class_path)
        self._policy = policy_cls()
        self.selected_coa = selected.coa.name
        self.selection_trace.append(
            {
                "num_agents": state.num_agents,
                "density": state.density,
                "selected_coa": selected.coa.name,
                "policy_class_path": selected.coa.policy_class_path,
                "score": selected.score,
                "rationale": selected.rationale,
                "failed_checks": list(selected.failed_checks),
            }
        )

    def act_many(self, handles, observations, **kwargs):
        env = observations[0]
        self._ensure_policy(env)
        return self._policy.act_many(handles, observations, **kwargs)

    def act(self, handle, observation, **kwargs):
        self._ensure_policy(observation)
        return self._policy.act(handle, observation, **kwargs)

    def reset(self, *args, **kwargs):
        if self._policy is not None and hasattr(self._policy, "reset"):
            self._policy.reset(*args, **kwargs)

