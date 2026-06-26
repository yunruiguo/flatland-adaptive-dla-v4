"""Candidate courses of action for Flatland."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CandidateCOA:
    """A high-level policy strategy candidate.

    In Flatland, a COA maps to a concrete `RailEnvPolicy` class rather than a
    natural-language pick/place sequence.
    """

    name: str
    policy_class_path: str
    rationale: str
    expected_strengths: tuple[str, ...] = ()
    risk_notes: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class COAEvaluation:
    """Validation and scoring result for one candidate."""

    coa: CandidateCOA
    valid: bool
    score: float
    failed_checks: tuple[str, ...] = ()
    rationale: str = ""

