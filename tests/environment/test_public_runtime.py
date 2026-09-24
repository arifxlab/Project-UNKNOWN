"""Tests for the public environment runtime.

These tests verify the public runtime boundary without exposing or depending
on hidden benchmark truth or evaluation state.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from unknown.environment.public.runtime import (
    EnvironmentNotInitializedError,
    EnvironmentRuntimeError,
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
        entity_count=2,
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


def test_reset_returns_projected_public_observation(
    config: PublicEnvironmentConfig,
) -> None:
    """Reset must return a projection of the deterministic world."""

    runtime = PublicEnvironmentRuntime()

    observation = runtime.reset(config=config, seed=42)

    assert observation.step_index == 0
    assert observation.observation_id == "observation-00000000"
    assert observation.kind.value == "state"
    assert len(observation.entities) == config.entity_count
    assert observation.relations
    assert observation.events == ()


def test_reset_is_deterministic_for_public_initial_state(
    config: PublicEnvironmentConfig,
) -> None:
    """Equivalent seeded resets must expose equivalent observations."""

    first = PublicEnvironmentRuntime()
    second = PublicEnvironmentRuntime()

    first_observation = first.reset(config=config, seed=123)
    second_observation = second.reset(config=config, seed=123)

    assert first_observation == second_observation


def test_different_seeds_produce_different_public_worlds(
    config: PublicEnvironmentConfig,
) -> None:
    """Different seeds should produce different observable initial states."""

    first = PublicEnvironmentRuntime()
    second = PublicEnvironmentRuntime()

    first_observation = first.reset(config=config, seed=123)
    second_observation = second.reset(config=config, seed=456)

    assert first_observation != second_observation


def test_observe_projects_current_world_state(
    config: PublicEnvironmentConfig,
) -> None:
    """Repeated observe calls return the current public projection."""

    runtime = PublicEnvironmentRuntime()

    first = runtime.reset(config=config, seed=42)
    second = runtime.observe()

    assert first == second


def test_public_observation_does_not_expose_internal_mass(
    config: PublicEnvironmentConfig,
) -> None:
    """Internal mass must not cross the runtime observation boundary."""

    runtime = PublicEnvironmentRuntime()

    observation = runtime.reset(config=config, seed=42)

    for entity in observation.entities:
        assert entity.attributes == {}
        assert "mass" not in repr(entity)


def test_public_observation_does_not_expose_internal_category(
    config: PublicEnvironmentConfig,
) -> None:
    """Internal semantic category must not cross the runtime boundary."""

    runtime = PublicEnvironmentRuntime()

    observation = runtime.reset(config=config, seed=42)

    for entity in observation.entities:
        assert "category" not in repr(entity)
        assert "AGENT" not in repr(entity)
        assert "OBJECT" not in repr(entity)
        assert "LANDMARK" not in repr(entity)


def test_no_op_step_advances_real_world(
    config: PublicEnvironmentConfig,
) -> None:
    """A valid action must advance the deterministic world."""

    runtime = PublicEnvironmentRuntime()

    initial = runtime.reset(config=config, seed=42)

    result = runtime.step(
        PublicAction(kind=ActionKind.NO_OP),
    )

    assert result.observation.step_index == 1
    assert result.observation.observation_id == "observation-00000001"
    assert result.reward == 0.0
    assert result.terminal is False
    assert runtime.is_terminal() is False

    assert result.observation.entities != initial.entities


def test_move_action_changes_public_observation(
    config: PublicEnvironmentConfig,
) -> None:
    """A public MOVE action must affect the projected world state."""

    runtime = PublicEnvironmentRuntime()

    initial = runtime.reset(config=config, seed=42)

    entity_id = initial.entities[0].entity_id

    result = runtime.step(
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id=entity_id,
            vector=PublicVector2(x=1.0, y=0.0),
        )
    )

    moved_entity = next(
        entity
        for entity in result.observation.entities
        if entity.entity_id == entity_id
    )

    initial_entity = next(
        entity
        for entity in initial.entities
        if entity.entity_id == entity_id
    )

    assert moved_entity.velocity.x == initial_entity.velocity.x + 1.0
    assert moved_entity.velocity.y == initial_entity.velocity.y


def test_move_action_requires_entity_id(
    config: PublicEnvironmentConfig,
) -> None:
    """MOVE actions require an entity identifier."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    with pytest.raises(InvalidPublicActionError):
        runtime.step(
            PublicAction(
                kind=ActionKind.MOVE,
                vector=PublicVector2(x=1.0, y=0.0),
            )
        )


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
                entity_id="entity-0000",
            )
        )


def test_disallowed_action_is_rejected() -> None:
    """Actions outside the configured public action set must fail."""

    config = PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=3,
        world_width=100.0,
        world_height=100.0,
        entity_count=2,
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
                entity_id="entity-000",
            )
        )


def test_set_position_intervention_changes_position_without_kinematics(
    config: PublicEnvironmentConfig,
) -> None:
    """SET_POSITION replaces position while preserving velocity."""

    runtime = PublicEnvironmentRuntime()
    initial = runtime.reset(config=config, seed=1)

    entity_id = initial.entities[0].entity_id
    initial_entity = initial.entities[0]

    result = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id=entity_id,
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    updated_entity = result.observation.entities[0]

    assert result.observation.step_index == 1
    assert updated_entity.position.x == 10.0
    assert updated_entity.position.y == 20.0
    assert updated_entity.velocity == initial_entity.velocity


def test_set_velocity_intervention_changes_velocity_without_kinematics(
    config: PublicEnvironmentConfig,
) -> None:
    """SET_VELOCITY replaces velocity while preserving position."""

    runtime = PublicEnvironmentRuntime()
    initial = runtime.reset(config=config, seed=1)

    entity_id = initial.entities[0].entity_id
    initial_entity = initial.entities[0]

    result = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_VELOCITY,
            entity_id=entity_id,
            vector=PublicVector2(x=7.0, y=-4.0),
        )
    )

    updated_entity = result.observation.entities[0]

    assert result.observation.step_index == 1
    assert updated_entity.position == initial_entity.position
    assert updated_entity.velocity.x == 7.0
    assert updated_entity.velocity.y == -4.0


def test_remove_entity_intervention_removes_entity_from_public_observation(
    config: PublicEnvironmentConfig,
) -> None:
    """REMOVE_ENTITY removes the selected entity from the projection."""

    runtime = PublicEnvironmentRuntime()
    initial = runtime.reset(config=config, seed=1)

    entity_id = initial.entities[0].entity_id

    result = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.REMOVE_ENTITY,
            entity_id=entity_id,
        )
    )

    remaining_ids = {
        entity.entity_id
        for entity in result.observation.entities
    }

    assert result.observation.step_index == 1
    assert entity_id not in remaining_ids
    assert len(result.observation.entities) == 1


def test_valid_intervention_advances_terminal_lifecycle(
    config: PublicEnvironmentConfig,
) -> None:
    """An intervention counts as one transition toward max_steps."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    first = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id="entity-000",
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    second = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_VELOCITY,
            entity_id="entity-001",
            vector=PublicVector2(x=2.0, y=3.0),
        )
    )

    third = runtime.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id="entity-001",
            vector=PublicVector2(x=30.0, y=40.0),
        )
    )

    assert first.terminal is False
    assert second.terminal is False
    assert third.terminal is True
    assert third.observation.step_index == config.max_steps
    assert runtime.is_terminal() is True


def test_invalid_intervention_entity_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """Interventions targeting missing entities must fail."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    before = runtime.observe()

    with pytest.raises(InvalidPublicInterventionError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-999",
                vector=PublicVector2(x=10.0, y=20.0),
            )
        )

    assert runtime.observe() == before


def test_remove_entity_rejects_vector(
    config: PublicEnvironmentConfig,
) -> None:
    """REMOVE_ENTITY must not accept a vector."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    with pytest.raises(InvalidPublicInterventionError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.REMOVE_ENTITY,
                entity_id="entity-000",
                vector=PublicVector2(x=1.0, y=1.0),
            )
        )


def test_set_position_out_of_bounds_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """SET_POSITION must reject positions outside the world."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    before = runtime.observe()

    with pytest.raises(InvalidPublicInterventionError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-000",
                vector=PublicVector2(x=101.0, y=20.0),
            )
        )

    assert runtime.observe() == before


def test_set_velocity_non_finite_value_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """SET_VELOCITY must reject non-finite values."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    with pytest.raises(InvalidPublicInterventionError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_VELOCITY,
                entity_id="entity-000",
                vector=PublicVector2(x=float("nan"), y=0.0),
            )
        )


def test_invalid_intervention_kind_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """Disallowed intervention kinds must fail before transition logic."""

    restricted_config = replace(
        config,
        allowed_intervention_kinds=(
            InterventionKind.SET_POSITION,
        ),
    )

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=restricted_config, seed=1)

    with pytest.raises(InvalidPublicInterventionError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.REMOVE_ENTITY,
                entity_id="entity-000",
            )
        )


def test_intervention_after_terminal_state_is_rejected(
    config: PublicEnvironmentConfig,
) -> None:
    """Interventions cannot be submitted after episode termination."""

    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=config, seed=1)

    for _ in range(config.max_steps):
        runtime.step(PublicAction(kind=ActionKind.NO_OP))

    with pytest.raises(EnvironmentTerminalError):
        runtime.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-000",
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

    invalid_config = replace(config, **{field_name: value})
    runtime = PublicEnvironmentRuntime()

    with pytest.raises(ValueError):
        runtime.reset(config=invalid_config, seed=1)


def test_runtime_does_not_expose_hidden_or_evaluation_attributes(
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


def test_runtime_does_not_return_world_state(
    config: PublicEnvironmentConfig,
) -> None:
    """Public runtime observations must never be WorldState objects."""

    runtime = PublicEnvironmentRuntime()

    observation = runtime.reset(config=config, seed=1)

    assert observation.__class__.__name__ == "PublicObservation"
    assert "WorldState" not in type(observation).__name__