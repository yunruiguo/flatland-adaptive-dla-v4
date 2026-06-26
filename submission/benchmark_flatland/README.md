# Flatland ECML-PKDD 2026 Challenge Adaptation

This module isolates the Flatland ECML-PKDD 2026 work from the existing
robotics, Isaac, AI2-THOR, and EB-ALFRED code.

Current phase:

1. Audit official challenge sources.
2. Run source-mode starter-kit smoke tests while Docker is unavailable.
3. Run maintained official baselines.
4. Implement Flatland-specific policy variants.
5. Validate improvements against the starter-kit curriculum.

The final submission policy must be CPU-only, self-contained, deterministic
where feasible, and compatible with the official `RailEnvPolicy` interface.

## Current Source-Mode Result

Docker validation is still pending because the official base image pull is
blocked by A100 proxy/GHCR access. Per user instruction, development continued
in source mode with all large files under `/mnt/data2`.

Measured on the 27-scenario starter-kit curriculum:

| Policy | Sum Normalized Reward | Mean Success Rate |
| --- | ---: | ---: |
| Official deadlock avoidance | 19.6358 | 0.8089 |
| Adaptive DLA v1 | 20.2952 | 0.8378 |

`AdaptiveDLA25LessElseEnteringPolicy` is the current best source-mode policy.
It uses less-conservative movement for dense 25-agent scenarios and
entering-prevention deadlock avoidance otherwise.

Evidence:

- `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/summary.json`
- `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/comparison_vs_deadlock_avoidance.csv`
- `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/report.md`

## Decision Pipeline Mapping

The Flatland module follows the same high-level platform architecture, adapted
to the railway domain and official challenge constraints.

```text
RailEnv observation
-> structured FlatlandWorldState
-> deterministic COA generation
-> policy schema/import validation
-> measured-prior scoring
-> executable RailEnvPolicy
-> trajectory analysis
```

Current implementation:

- `state/state_adapter.py`: converts `RailEnv` into `FlatlandWorldState`.
- `planning/coa_generator.py`: generates candidate policy-family COAs.
- `validation/coa_validator.py`: validates that COAs map to executable policy
  classes and basic environment preconditions.
- `planning/policy_selector.py`: scores candidates using measured source-mode
  evidence and scenario features.
- `policy/flatland_decision_policy.py`: official-interface wrapper that
  selects and executes the best validated policy.

Unlike EB-ALFRED, Flatland challenge submission must be self-contained and
CPU-only, so there is no runtime LLM call. The COA generator is deterministic,
but it occupies the same architectural role as LLM-generated candidate plans in
the embodied decision platform.
