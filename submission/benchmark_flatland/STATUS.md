# Flatland ECML-PKDD 2026 Status

## 2026-06-24

- Created isolated `benchmark_flatland/` module.
- Created local branch `flatland-ecml2026`.
- Started official challenge audit.
- A100 server is reachable and `/mnt/data2` is mounted with sufficient space.
- Docker is installed on A100.
- Official repositories cloned on A100:
  - `/mnt/data2/src/ecml2026-starterkit`
  - `/mnt/data2/src/flatland-rl`
  - `/mnt/data2/src/flatland-baselines`
- Official source audit logs saved under
  `/mnt/data2/outputs/flatland2026/audit/`.
- Docker daemon initially had a stale proxy configuration pointing at
  `127.0.0.1:8070`; no proxy service was listening.
- Temporarily disabled the stale Docker daemon proxy and confirmed GHCR access;
  then restored the original Docker proxy config.
- Official Docker build started pulling
  `ghcr.io/flatland-association/flatland-baselines:v4.2.6`, but direct
  download was too slow for interactive completion.
- `flatland2026` conda environment creation is blocked by HTTP 403 from
  `repo.anaconda.com/pkgs/main`.
- Per user instruction, Docker was skipped for continued development.
- Created data-disk Python virtual environment:
  `/mnt/data2/envs/flatland2026_venv`.
- Installed `flatland-rl==4.2.6` with pip cache under
  `/mnt/data2/pip_cache/flatland2026`.
- Ran source-mode baseline smoke tests on `level_0_scenario_1.pkl`:
  - starter-kit random: success rate `0.5000`, normalized reward `0.0000`
  - forward-only: success rate `0.3333`, normalized reward `0.3067`
  - deadlock avoidance: success rate `1.0000`, normalized reward `0.5128`
- Generated source-mode baseline outputs under
  `/mnt/data2/outputs/flatland2026/baselines/`.
- Generated representative replay artifacts:
  - `/mnt/data2/outputs/flatland2026/baselines/representative_replay.mp4`
  - `/mnt/data2/outputs/flatland2026/baselines/representative_replay.gif`
- Ran the 27-scenario starter-kit curriculum in source mode with the
  maintained deadlock-avoidance baseline:
  - mean success rate `0.8089`
  - mean normalized reward `0.7273`
  - sum normalized reward `19.6358`
  - fully solved `17 / 27` scenarios
  - `2 / 27` scenarios fell below the 25% completion threshold
  - outputs saved under `/mnt/data2/outputs/flatland2026/baselines/`

## Immediate Next Steps

1. Implement the first Flatland-specific decision policy in source mode.
2. Target the curriculum failure cases where deadlock avoidance falls below
   the 25% completion threshold.
3. Compare our policy against the measured deadlock-avoidance baseline on the
   same scenario and then the starter-kit curriculum.
4. Keep all generated trajectories, caches, and reports under `/mnt/data2`.
5. For final official validation, start/restore a working A100 proxy on
   `127.0.0.1:8070` or otherwise improve access to GHCR.
6. Rerun the unchanged starter-kit Docker build:
   `docker build -t flatland2026/starterkit-random:ac8b1fd -f Dockerfile .`
7. Run the official single-scenario smoke command with `ECML2026Rewards`.
8. Run `flatland-trajectory-analysis` on the generated trajectory output.

## Objective 1 Status

Partially complete in source mode. Official Docker validation remains pending.

- Source-mode official scenario execution: complete.
- Source-mode trajectory analysis: complete.
- Source-mode non-random baseline score: complete.
- Source-mode curriculum run: complete.
- Official Docker image build: pending due A100 Docker proxy/GHCR access.
- Official leaderboard result: not attempted.

## 2026-06-25

- Implemented Flatland policy variants under `benchmark_flatland/policy/`.
- Tested targeted variants on known weak curriculum scenarios.
- Full curriculum result for global less-conservative policy:
  - sum normalized reward `19.9873`
  - beats base deadlock avoidance by `+0.3515`
- Full curriculum result for global entering-prevention policy:
  - sum normalized reward `20.1129`
  - beats base deadlock avoidance by `+0.4771`
- Implemented adaptive portfolio policy:
  `AdaptiveDLA25LessElseEnteringPolicy`
  - uses less-conservative movement for dense `>=25` agent scenarios
  - uses entering-prevention policy otherwise
- Confirmed full 27-scenario curriculum result for adaptive policy:
  - sum normalized reward `20.2952`
  - mean normalized reward `0.7517`
  - mean success rate `0.8378`
  - improvement over base deadlock avoidance: `+0.6594`
- Adaptive policy outputs:
  - `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/summary.json`
  - `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/curriculum_results.csv`
  - `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/comparison_vs_deadlock_avoidance.csv`
  - `/mnt/data2/outputs/flatland2026/baselines/adaptive_dla_v1/report.md`
- Refactored Flatland policy selection to follow the platform Decision
  Pipeline architecture:
  - `state/state_adapter.py`
  - `planning/coa_generator.py`
  - `validation/coa_validator.py`
  - `planning/policy_selector.py`
  - `policy/flatland_decision_policy.py`
- `AdaptiveDLA25LessElseEnteringPolicy` now delegates through
  `FlatlandDecisionPolicy`.
- Architecture smoke test passed on `00_scene_1_ll-2_a-1`:
  - success rate `1.0`
  - normalized reward `1.0`
  - output: `/mnt/data2/outputs/flatland2026/architecture_smoke_adaptive_policy`
