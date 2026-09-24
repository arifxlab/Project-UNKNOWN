"""Shared test helpers for Project UNKNOWN environment tests."""

from __future__ import annotations

from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    PublicEnvironmentConfig,
)


def make_config(
    *,
    max_steps: int = 10,
    world_width: float = 100.0,
    world_height: float = 80.0,
    entity_count: int = 4,
    observation_history_limit: int = 10,
    allowed_action_kinds: tuple[ActionKind, ...] = (
        ActionKind.NO_OP,
        ActionKind.MOVE,
        ActionKind.INTERACT,
    ),
    allowed_intervention_kinds: tuple[InterventionKind, ...] = (
        InterventionKind.SET_POSITION,
        InterventionKind.SET_VELOCITY,
        InterventionKind.REMOVE_ENTITY,
    ),
) -> PublicEnvironmentConfig:
    """Create a valid public environment configuration for tests."""

    return PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=max_steps,
        world_width=world_width,
        world_height=world_height,
        entity_count=entity_count,
        observation_history_limit=observation_history_limit,
        allowed_action_kinds=allowed_action_kinds,
        allowed_intervention_kinds=allowed_intervention_kinds,
        public_attributes=(),
    )