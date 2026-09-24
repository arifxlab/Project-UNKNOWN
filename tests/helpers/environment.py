"""Shared test helpers for Project UNKNOWN environment tests."""
from __future__ import annotations

from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    PublicEnvironmentConfig,
)


def make_config(
    *,
    entity_count: int = 4,
    max_steps: int = 20,
    allowed_action_kinds: tuple[ActionKind, ...] = (
        ActionKind.NO_OP,
        ActionKind.MOVE,
        ActionKind.INTERACT,
    ),
) -> PublicEnvironmentConfig:
    """Create a valid configuration for deterministic-world tests."""
    return PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        world_width=100.0,
        world_height=80.0,
        max_steps=max_steps,
        entity_count=entity_count,
        observation_history_limit=10,
        allowed_action_kinds=allowed_action_kinds,
        allowed_intervention_kinds=(
            InterventionKind.SET_POSITION,
            InterventionKind.SET_VELOCITY,
            InterventionKind.REMOVE_ENTITY,
        ),
        public_attributes=(
            "position",
            "velocity",
            "mass",
            "category",
            "relations",
        ),
    )