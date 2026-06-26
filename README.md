# Flatland Adaptive Decision Pipeline v6

Submit image target:

```text
ghcr.io/yunruiguo/flatland-adaptive-dla-v6:latest
```

This repository contains the minimal Flatland submission image source for the
Decision Pipeline v6 candidate.

## Local Validation Evidence

Validated on A100 before publication:

- Full 27-scenario curriculum output:
  `/mnt/data2/outputs/flatland2026/adaptive_dla_v6/`
- Sum normalized reward: `20.428280906501694`
- Mean normalized reward: `0.7566029965370998`
- Mean success rate: `0.8577777777777779`
- Improvement over v5 sum normalized reward: `+0.01070537684609`

Focused improvement over v5:

- `15_scene_1_ll-3_a-25`: `0.3200652528548123` -> `0.3305709624796085`
- `06_scene_1_ll-2_a-25`: `0.4652911813643926` -> `0.4654908485856905`

Docker smoke test:

- Image: `submission/flatland-adaptive-dla-v6:latest`
- Image ID prefix: `95d5f74121d9`
- Smoke scenario: `15_scene_1_ll-3_a-25`
- Smoke success rate: `0.64`
- Smoke normalized reward: `0.3305709624796085`
- Smoke output:
  `/mnt/data2/outputs/flatland2026/docker_smoke_v6_scene15_20260626_131526_analysis`

## Publishing

The GitHub Actions workflow builds and pushes:

```text
ghcr.io/yunruiguo/flatland-adaptive-dla-v6:latest
```

The workflow uses `GITHUB_TOKEN` with `packages: write`, avoiding the need for
a local personal token with `write:packages`.
