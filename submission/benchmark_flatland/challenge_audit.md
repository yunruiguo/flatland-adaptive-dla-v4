# Flatland ECML-PKDD 2026 Challenge Audit

Audit status: in progress. This file records evidence from official sources
only. It must not claim leaderboard or record-breaking results without official
submission evidence.

## Official Sources

- Starter kit: https://github.com/flatland-association/ecml2026-starterkit
- Flatland RL: https://github.com/flatland-association/flatland-rl
- Flatland baselines: https://github.com/flatland-association/flatland-baselines
- Flatland book documentation:
  https://flatland-association.github.io/flatland-book/challenges/ecml2026.html
- Evaluation documentation:
  https://flatland-association.github.io/flatland-book/challenges/ecml2026/eval.html
- Competition portal: https://competition.flatland.cloud/

## Repository Snapshot

Repositories were cloned on A100 under `/mnt/data2/src`.

| Repository | Path | Commit |
| --- | --- | --- |
| ecml2026-starterkit | `/mnt/data2/src/ecml2026-starterkit` | `ac8b1fdeda2b7e8409a9bd61f16c45b8525c228d` |
| flatland-rl | `/mnt/data2/src/flatland-rl` | `bcff919593141fc6b6e0ca117637da8b557f3e98` |
| flatland-baselines | `/mnt/data2/src/flatland-baselines` | `c5b344d43e231e26e54520732e0f63d6796785a7` |

Remote audit logs:

- `/mnt/data2/outputs/flatland2026/audit/starterkit_inspection.txt`
- `/mnt/data2/outputs/flatland2026/audit/starterkit_runtime_files.txt`
- `/mnt/data2/outputs/flatland2026/audit/flatland_rl_key_files.txt`
- `/mnt/data2/outputs/flatland2026/audit/flatland_rl_api_rewards.txt`
- `/mnt/data2/outputs/flatland2026/audit/flatland_baselines_inspection.txt`
- `/mnt/data2/outputs/flatland2026/audit/docker_build_starterkit_random.log`

## Verified Challenge Facts

- Supported Flatland versions in the official documentation: `4.2.5` and
  `4.2.6`.
- Starter-kit Dockerfile builds from
  `ghcr.io/flatland-association/flatland-baselines:v4.2.6`.
- Submission format is a Docker image submitted through the competition portal.
- The starter-kit policy entrypoint is the official `RailEnvPolicy` interface.
- `RailEnvPolicy` supports `act` and can optionally implement `act_many`.
- The starter-kit default policy is random:
  `submission/my_policy.py` aliases `MyPolicy = RandomPolicy`.
- `submission/requirements.txt` pins `flatland-rl==4.2.6`.
- Official action enum from `RailEnvActions`:
  `DO_NOTHING=0`, `MOVE_LEFT=1`, `MOVE_FORWARD=2`, `MOVE_RIGHT=3`,
  `STOP_MOVING=4`.
- Official scoring uses `flatland.envs.rewards.ECML2026Rewards`.
- The documentation states a single scenario reward is normalized to `[-1, 1]`.
- Submission score is the sum of scenario scores.
- If fewer than 25% of agents arrive in a level, subsequent levels are not
  evaluated.
- Runtime limits from official documentation: 4 CPU cores, 15 GB RAM, no GPU,
  30 minutes per scenario, 5 hours total submission time.
- Daily submission limit from official documentation: 2 submissions.
- Listed competition end in the documentation: 2026-06-29 AoE
  (verified 2026-06-25).

## ECML2026Rewards Factors

Verified in `/mnt/data2/src/flatland-rl/flatland/envs/rewards.py`:

- `cancellation_factor = 5.0`
- `cancellation_time_buffer = 0.0`
- `target_not_reached_minimum_penalty = 100.0`
- `intermediate_not_served_penalty = 50.0`
- `intermediate_late_arrival_penalty_factor = 0.5`
- `intermediate_early_departure_penalty_factor = 0.5`
- `collision_factor = 250.0`

The reward implementation caps per-agent negative rewards and normalizes by
`max_episode_steps * num_agents`.

## Official Starter-Kit Smoke Status

Attempted command on A100:

```bash
cd /mnt/data2/src/ecml2026-starterkit
docker build -t flatland2026/starterkit-random:ac8b1fd -f Dockerfile .
```

Observed infrastructure issue:

- Docker was configured with a stale daemon proxy:
  `/etc/systemd/system/docker.service.d/http-proxy.conf`
  using `127.0.0.1:8070`.
- No proxy service was listening on port `8070`.
- Direct `curl -I https://ghcr.io/v2/` succeeded.
- The stale Docker proxy was disabled temporarily and Docker was restarted.
- The GHCR pull then started successfully, proving the image is reachable.
- Direct download speed was too low for interactive completion: after about
  209 seconds the largest base layer had reached only about `37.75 MB / 6.45 GB`.
- The original Docker proxy configuration was restored after the test.

Current blocker: official Docker smoke has not completed because the official
base image pull is network-bound on A100. Start/restore a working local proxy
on `127.0.0.1:8070` or pre-pull
`ghcr.io/flatland-association/flatland-baselines:v4.2.6`, then rerun the
unchanged starter-kit Docker build.

## Source-Mode Smoke and Baselines

Per user instruction on 2026-06-24, Docker was skipped for continued
development. A Python virtual environment was created on the data disk:

- Environment: `/mnt/data2/envs/flatland2026_venv`
- Pip cache: `/mnt/data2/pip_cache/flatland2026`
- Installed Flatland version: `4.2.6`

The official example scenario was run in source mode:

- Scenario:
  `/mnt/data2/src/ecml2026-starterkit/reinforcement_learning/sampling/level_0_scenario_1.pkl`
- Reward argument: `flatland.envs.rewards.ECML2026Rewards`
- Seed handling: `--post-seed 42` because the Flatland CLI rejects `--seed`
  together with `--env-path`.

Source-mode results:

| Baseline | Success Rate | Normalized Reward | Env Time |
| --- | ---: | ---: | ---: |
| starter-kit random | 0.5000 | 0.0000 | 493 |
| forward-only heuristic | 0.3333 | 0.3067 | 493 |
| deadlock-avoidance heuristic | 1.0000 | 0.5128 | 204 |

The maintained deadlock-avoidance baseline is materially better than the
starter-kit random policy on the example scenario.

Generated baseline package:

- `/mnt/data2/outputs/flatland2026/baselines/baseline_summary.csv`
- `/mnt/data2/outputs/flatland2026/baselines/scenario_results.json`
- `/mnt/data2/outputs/flatland2026/baselines/all_trains_arrived.csv`
- `/mnt/data2/outputs/flatland2026/baselines/normalized_reward_by_scenario.csv`
- `/mnt/data2/outputs/flatland2026/baselines/runtime_by_scenario.csv`
- `/mnt/data2/outputs/flatland2026/baselines/completion_by_level.csv`
- `/mnt/data2/outputs/flatland2026/baselines/failure_taxonomy.json`
- `/mnt/data2/outputs/flatland2026/baselines/representative_replay.mp4`
- `/mnt/data2/outputs/flatland2026/baselines/representative_replay.gif`
- `/mnt/data2/outputs/flatland2026/baselines/baseline_report.md`

Source-mode curriculum results for maintained deadlock-avoidance baseline:

- Curriculum scenarios: `27`
- Mean success rate: `0.8089`
- Mean normalized reward: `0.7273`
- Sum normalized reward: `19.6358`
- Fully solved scenarios: `17 / 27`
- Partial scenarios at or above 25% completion: `8 / 27`
- Partial scenarios below 25% completion: `2 / 27`

Curriculum output files:

- `/mnt/data2/outputs/flatland2026/baselines/curriculum_deadlock_avoidance_results.csv`
- `/mnt/data2/outputs/flatland2026/baselines/curriculum_completion_by_level.csv`
- `/mnt/data2/outputs/flatland2026/baselines/curriculum_normalized_reward_by_scenario.csv`
- `/mnt/data2/outputs/flatland2026/baselines/curriculum_runtime_by_scenario.csv`
- `/mnt/data2/outputs/flatland2026/baselines/curriculum_failure_taxonomy.json`
- `/mnt/data2/outputs/flatland2026/baselines/curriculum_summary.json`
- `/mnt/data2/outputs/flatland2026/baselines/curriculum_report.md`

Movie callback note: the official callback generated PNG frames but failed to
assemble MP4 because system `ffmpeg` is not installed. To avoid root-disk and
system package changes, the MP4/GIF replay artifacts were assembled using
`imageio` and `imageio-ffmpeg` installed inside the data-disk virtual
environment.

Important caveat: these are reproducible source-mode results, not official
Docker-gated or leaderboard scores.

## Conda Environment Status

The required separate conda environment `flatland2026` is not yet available.
An attempted `conda create -n flatland2026 python=3.12` failed because the A100
received HTTP 403 from `https://repo.anaconda.com/pkgs/main`. This is a network
or conda channel access issue, not a project-code issue.

## Official Baselines

The maintained `flatland-baselines` repository was cloned and inspected.
Available baseline families include:

- random
- do-nothing heuristic
- forward-only heuristic
- forever heuristic
- shortest-path/deadlock-avoidance heuristic

Docker-gated baseline execution is pending the official Docker image
availability. Source-mode baseline execution has completed as recorded above.

## Leaderboard Status

The public leaderboard has not yet been retrieved. If
`https://competition.flatland.cloud/` requires authentication, record that fact
in `leaderboard_snapshot.json` and continue local reproducible evaluation until
an official submission is required.
