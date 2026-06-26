# Flatland Adaptive Decision Pipeline v4

Submit image target:

```text
ghcr.io/yunruiguo/flatland-adaptive-dla-v4:latest
```

This repository contains the minimal Flatland submission image source for the
Decision Pipeline v4 candidate.

## Local Validation Evidence

Validated on A100 before publication:

- Full 27-scenario curriculum output:
  `/mnt/data2/outputs/flatland2026/adaptive_dla_v4/`
- Sum normalized reward: `20.34883637607562`
- Mean normalized reward: `0.7536606065213193`
- Mean success rate: `0.8637037037037038`
- Improvement over stored v1 sum normalized reward: `+0.05362453512194065`

Docker smoke test:

- Image ID prefix: `9b92fdd2696a`
- Smoke success rate: `1.0`
- Smoke normalized reward: `0.5128205128205128`
- Smoke output:
  `/mnt/data2/outputs/flatland2026/docker_smoke_v4_rerun_20260626_093618_analysis`

## Publishing

The GitHub Actions workflow builds and pushes:

```text
ghcr.io/yunruiguo/flatland-adaptive-dla-v4:latest
```

The workflow uses `GITHUB_TOKEN` with `packages: write`, avoiding the need for
a local personal token with `write:packages`.
