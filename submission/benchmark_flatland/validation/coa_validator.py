"""Schema and feasibility checks for Flatland policy COAs."""

from __future__ import annotations

import importlib

from benchmark_flatland.planning.candidate_coa import CandidateCOA, COAEvaluation
from benchmark_flatland.state.railway_state import FlatlandWorldState


def _class_importable(path: str) -> bool:
    module_name, _, class_name = path.rpartition(".")
    if not module_name or not class_name:
        return False
    module = importlib.import_module(module_name)
    return hasattr(module, class_name)


def validate_coa_schema(coa: CandidateCOA, state: FlatlandWorldState) -> COAEvaluation:
    """Check that a generated COA can become an executable policy."""

    failed = []
    if not coa.name:
        failed.append("missing_name")
    if not coa.policy_class_path:
        failed.append("missing_policy_class_path")
    else:
        try:
            if not _class_importable(coa.policy_class_path):
                failed.append("policy_class_not_found")
        except Exception as exc:  # pragma: no cover - diagnostic path
            failed.append(f"policy_class_import_error:{type(exc).__name__}")
    if state.num_agents <= 0:
        failed.append("no_agents")
    if state.width <= 0 or state.height <= 0:
        failed.append("invalid_grid_size")

    return COAEvaluation(
        coa=coa,
        valid=not failed,
        score=0.0,
        failed_checks=tuple(failed),
        rationale="schema/import validation",
    )

