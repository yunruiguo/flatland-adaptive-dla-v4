"""Observation builder for the Flatland Decision Pipeline submission.

The policy selects a strategy from scenario-level RailEnv metadata. Returning the
current environment as the observation keeps the policy compatible with the
official `RailEnvPolicy.act_many(handles, observations=...)` interface without
adding external dependencies.
"""

from __future__ import annotations

from flatland.core.env_observation_builder import ObservationBuilder


class EnvObservationBuilder(ObservationBuilder):
    """Return the current RailEnv object as each agent observation."""

    def reset(self):
        return None

    def get(self, handle=0):
        return self.env


MyObservationBuilder = EnvObservationBuilder
