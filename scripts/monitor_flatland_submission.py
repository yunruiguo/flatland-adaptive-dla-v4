from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


API_ROOT = "https://api-competition.flatland.cloud"
TARGET_BENCHMARK_ID = "c85d5fc2-15da-4a62-8e14-28d1261c29bd"
DEFAULT_IMAGE = "ghcr.io/yunruiguo/flatland-adaptive-dla-v6:latest"


@dataclass(frozen=True)
class SubmissionScore:
    submission_id: str
    name: str
    image: str
    status: str | None
    submitted_at: str | None
    normalized_reward: float | None
    percentage_complete: float | None


def get_json(path: str) -> dict[str, Any]:
    with urllib.request.urlopen(f"{API_ROOT}{path}", timeout=30) as response:
        return json.load(response)


def get_submissions() -> list[dict[str, Any]]:
    data = get_json("/submissions")
    body = data.get("body", data)
    if not isinstance(body, list):
        raise RuntimeError("Unexpected submissions response shape")
    return body


def get_score(submission_id: str) -> tuple[float | None, float | None]:
    try:
        data = get_json(f"/results/submissions/{submission_id}")
    except (TimeoutError, urllib.error.HTTPError, urllib.error.URLError):
        return None, None
    body = data.get("body", [])
    if not body:
        return None, None
    scores = {}
    for scoring in body[0].get("scorings", []):
        scores[scoring.get("field_key")] = scoring.get("score")
    return scores.get("normalized_reward"), scores.get("percentage_complete")


def collect_scores(submissions: list[dict[str, Any]]) -> list[SubmissionScore]:
    scored = []
    for submission in submissions:
        if submission.get("benchmark_id") != TARGET_BENCHMARK_ID:
            continue
        normalized_reward, percentage_complete = get_score(submission["id"])
        scored.append(
            SubmissionScore(
                submission_id=submission["id"],
                name=submission.get("name") or "",
                image=submission.get("submission_data_url") or "",
                status=submission.get("status"),
                submitted_at=submission.get("submitted_at"),
                normalized_reward=normalized_reward,
                percentage_complete=percentage_complete,
            )
        )
    return scored


def print_status(image: str) -> bool:
    submissions = get_submissions()
    matches = [s for s in submissions if s.get("submission_data_url") == image]
    print(f"target_image={image}")
    print(f"matching_submissions={len(matches)}")

    scored = collect_scores(submissions)
    scored_with_reward = [s for s in scored if s.normalized_reward is not None]
    scored_with_reward.sort(key=lambda s: s.normalized_reward or float("-inf"), reverse=True)

    if not matches:
        print("status=not_submitted")
        print("\nSubmit this image URL in the Flatland portal:")
        print(image)
        return False

    match_ids = {s["id"] for s in matches}
    for match in matches:
        normalized_reward, percentage_complete = get_score(match["id"])
        rank = None
        if normalized_reward is not None:
            better = sum(
                1
                for score in scored_with_reward
                if score.normalized_reward is not None and score.normalized_reward > normalized_reward
            )
            rank = better + 1
        print(
            json.dumps(
                {
                    "submission_id": match["id"],
                    "name": match.get("name"),
                    "status": match.get("status"),
                    "submitted_at": match.get("submitted_at"),
                    "normalized_reward": normalized_reward,
                    "percentage_complete": percentage_complete,
                    "rank_among_scored_public_submissions": rank,
                },
                indent=2,
            )
        )

    print("\nTop public scored submissions:")
    for index, score in enumerate(scored_with_reward[:10], start=1):
        marker = " <-- target" if score.submission_id in match_ids else ""
        print(
            f"{index:02d}. reward={score.normalized_reward} "
            f"complete={score.percentage_complete} name={score.name} image={score.image}{marker}"
        )
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor Flatland public submission score and rank.")
    parser.add_argument("--image", default=DEFAULT_IMAGE)
    parser.add_argument("--poll-seconds", type=int, default=0)
    parser.add_argument("--max-polls", type=int, default=1)
    args = parser.parse_args()

    for poll_index in range(args.max_polls):
        if poll_index:
            time.sleep(args.poll_seconds)
        submitted = print_status(args.image)
        if submitted:
            return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
