# Flatland Adaptive Decision Pipeline v5

Submit image target:

```text
ghcr.io/yunruiguo/flatland-adaptive-dla-v5:latest
```

This repository contains the minimal Flatland submission image source for the
Decision Pipeline v5 candidate.

## Local Validation Evidence

Validated on A100 before publication:

- Full 27-scenario curriculum output:
  `/mnt/data2/outputs/flatland2026/adaptive_dla_v5/`
- Sum normalized reward: `20.417575529655604`
- Mean normalized reward: `0.7562065010983557`
- Mean success rate: `0.8592592592592593`
- Improvement over v4 sum normalized reward: `+0.068739153579984`

Focused improvement over v4:

- `07_scene_4_ll-2_a-25`: `0.3786851211072665` -> `0.4368858131487889`
- `08_scene_5_ll-2_a-25`: `0.4721538461538461` -> `0.4826923076923076`

Docker smoke test:

- Image: `submission/flatland-adaptive-dla-v5:latest`
- Image ID prefix: `bec05a2a6230`
- Smoke scenario: `07_scene_4_ll-2_a-25`
- Smoke success rate: `0.32`
- Smoke normalized reward: `0.4368858131487889`
- Smoke output:
  `/mnt/data2/outputs/flatland2026/docker_smoke_v5_scene07_20260626_111523_analysis`

## Publishing

The GitHub Actions workflow builds and pushes:

```text
ghcr.io/yunruiguo/flatland-adaptive-dla-v5:latest
```

The workflow uses `GITHUB_TOKEN` with `packages: write`, avoiding the need for
a local personal token with `write:packages`.
