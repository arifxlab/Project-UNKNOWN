"""Tests for the public environment runtime.

These tests verify the public runtime contract without exposing or depending
on hidden benchmark truth or evaluation state.
"""

from __future__ import annotations

import pytest

from unknown.environment.public.runtime import (
    EnvironmentNotInitializedError,
    EnvironmentTerminalError,
    InvalidPublicActionError,
    InvalidPublicInterventionError,
    PublicEnvironmentRuntime,
)
from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    PublicAction,
    PublicEnvironmentConfig,
    PublicIntervention,
    PublicVector2,
)


@pytest.fixture
def config() -> PublicEnvironmentConfig:
    """Return a minimal valid public environment configuration."""
    return PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=3,
        world_width=100.0,
        world_height=100.0,
        entity_count=0,
        observation_history_limit=10,
        allowed_action_kinds=(
            ActionKind.NO_OP,
            ActionKind.MOVE,
            ActionKind.INTERACT,
        ),
        allowed_intervention_kinds=(
            InterventionKind.SET_POSITION,
            InterventionKind.SET_VELOCITY,
            InterventionKind.REMOVE_ENTITY,
        ),
        public_attributes=(),
    )


def test_runtime_requires_reset_before_observation() -> None:
    """Observation before initialization must fail explicitly."""
    runtime = PublicEnvironmentRuntime()

    with pytest.raises(EnvironmentNotInitializedError):
        runtime.observe()


def test_runtime_requires_reset_before_terminal_check() -> None:
    """Terminal state cannot be queried before initialization."""
    runtime = PublicEnvironmentRuntime()

    with pytest.raises(EnvironmentNotInitializedError):
        runtime.is_terminal()


def test_runtime_requires_reset_before_metadata() -> None:
    """Episode metadata cannot be queried before initialization."""
    runtime = PublicEnvironmentRuntime()

    with pytest.raises(EnvironmentNotInitializedError):
        runtime.episode_metadata()


def test_reset_returns_public_observation(
    config: PublicEnvironmentConfig,
) -> None:
    """Reset must return a public observation."""
    runtime = PublicEnvironmentRuntime()

    observation = runtime.reset(config=config, seed=42)

    assert observation.step_index == 0
    assert observation.observation_id == "observation-000000"
    assert observation.kind.value == "state"
    assert observation.entities == ()
    assert observation.relations == ()
    assert observation.events == ()


def test_reset_is_deterministic_for_public_initial_state(
    config: PublicEnvironmentConfig,
) -> None:
    """Equivalent resets must expose equivalent initial public state."""
    first = PublicEnvironmentRuntime()
    second = PublicEnvironmentRuntime()

    first_observation = first.reset(config=config, seed=123)
    second_observation = second.reset(config=config, seed=123)

    assert first_observation == second_observation


def test_episode_metadata_exposes_only_public_metadata(
    config: PublicEnvironmentConfig,
) -> None:
    """Episode metadata must contain only the public contract."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=7)

    metadata = runtime.episode_metadata()

    assert metadata.experiment_id == "opaque-experiment-001"
    assert metadata.environment_version == "0.1.0"
    assert metadata.schema_version == "0.1.0"
    assert metadata.max_steps == 3
    assert metadata.action_kinds == config.allowed_action_kinds
    assert metadata.intervention_kinds == config.allowed_intervention_kinds


def test_no_op_step_advances_episode(
    config: PublicEnvironmentConfig,
) -> None:
    """A valid public action must advance the episode."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    result = runtime.step(
        PublicAction(kind=ActionKind.NO_OP),
    )

    assert result.observation.step_index == 1
    assert result.observation.observation_id == "observation-000001"
    assert result.reward == 0.0
    assert result.terminal is False
    assert runtime.is_terminal() is False


def test_move_action_requires_vector(
    config: PublicEnvironmentConfig,
) -> None:
    """MOVE actions must provide their required public vector."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    with pytest.raises(InvalidPublicActionError):
        runtime.step(
            PublicAction(
                kind=ActionKind.MOVE,
            )
        )


def test_move_action_with_vector_is_accepted(
    config: PublicEnvironmentConfig,
) -> None:
    """A valid MOVE action must be accepted by the public contract."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    result = runtime.step(
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-001",
            vector=PublicVector2(x=1.0, y=0.0),
        )
    )

    assert result.observation.step_index == 1
    assert result.terminal is False


def test_disallowed_action_is_rejected() -> None:
    """Actions outside the configured public action set must fail."""
    config = PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=3,
        world_width=100.0,
        world_height=100.0,
        entity_count=0,
        observation_history_limit=10,
        allowed_action_kinds=(ActionKind.NO_OP,),
        allowed_intervention_kinds=(
            InterventionKind.SET_POSITION,
        ),
        public_attributes=(),
    )

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    with pytest.raises(InvalidPublicActionError):
        runtime.step(
            PublicAction(
                kind=ActionKind.INTERACT,
            )
        )


def test_position_intervention_requires_vector(
    config: PublicEnvironmentConfig,
) -> None:
    """SET_POSITION interventions must provide a vector."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    with pytest.raises(InvalidPublicInterventionError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-001",
            )
        )


def test_valid_position_intervention_is_accepted(
    config: PublicEnvironmentConfig,
) -> None:
    """A valid position intervention must advance the episode."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    result = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id="entity-001",
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    assert result.observation.step_index == 1
    assert result.terminal is False


def test_terminal_state_is_reached_at_max_steps(
    config: PublicEnvironmentConfig,
) -> None:
    """The runtime must terminate exactly at the configured step limit."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    runtime.step(PublicAction(kind=ActionKind.NO_OP))
    runtime.step(PublicAction(kind=ActionKind.NO_OP))
    result = runtime.step(PublicAction(kind=ActionKind.NO_OP))

    assert result.observation.step_index == config.max_steps
    assert result.terminal is True
    assert runtime.is_terminal() is True


def test_step_after_terminal_state_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """No action may be applied after episode termination."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    for _ in range(config.max_steps):
        runtime.step(PublicAction(kind=ActionKind.NO_OP))

    with pytest.raises(EnvironmentTerminalError):
        runtime.step(PublicAction(kind=ActionKind.NO_OP))


def test_intervention_after_terminal_state_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """No intervention may be applied after episode termination."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    for _ in range(config.max_steps):
        runtime.step(PublicAction(kind=ActionKind.NO_OP))

    with pytest.raises(EnvironmentTerminalError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-001",
                vector=PublicVector2(x=0.0, y=0.0),
            )
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("max_steps", 0),
        ("world_width", 0.0),
        ("world_height", 0.0),
        ("observation_history_limit", 0),
        ("entity_count", -1),
    ],
)
def test_invalid_configuration_is_rejected(
    config: PublicEnvironmentConfig,
    field_name: str,
    value: int | float,
) -> None:
    """Invalid public configuration values must be rejected."""
    from dataclasses import replace

    invalid_config = replace(config, **{field_name: value})
    runtime = PublicEnvironmentRuntime()

    with pytest.raises(ValueError):
        runtime.reset(config=invalid_config, seed=1)


def test_public_runtime_does_not_expose_hidden_or_evaluation_attributes(
    config: PublicEnvironmentConfig,
) -> None:
    """Runtime instance must not expose benchmark truth attributes."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    forbidden_names = {
        "hidden_state",
        "ground_truth",
        "ground_truth_representation",
        "condition",
        "benchmark_condition",
        "evaluation",
        "evaluation_record",
        "discovery_evaluation",
        "oracle",
    }

    assert forbidden_names.isdisjoint(vars(runtime))