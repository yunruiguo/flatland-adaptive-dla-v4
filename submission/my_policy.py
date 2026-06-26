"""Official Flatland ECML 2026 submission entry point.

This exposes the frozen source-mode best policy through the starter-kit
`MyPolicy` convention. The submission directory is added to `sys.path` so the
packaged `benchmark_flatland` module can keep its project-local imports.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SUBMISSION_DIR = Path(__file__).resolve().parent
if str(_SUBMISSION_DIR) not in sys.path:
    sys.path.insert(0, str(_SUBMISSION_DIR))

from benchmark_flatland.policy.deadlock_portfolio_policy import (  # noqa: E402
    AdaptiveDLA25LessElseEnteringPolicy,
)

MyPolicy = AdaptiveDLA25LessElseEnteringPolicy
