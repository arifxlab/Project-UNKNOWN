"""Tests for the deterministic synthetic world."""

from __future__ import annotations

import pytest

from unknown.environment.dynamics import (
    DeterministicWorld,
    InvalidWorldActionError,
    WorldNotInitializedError,
    WorldTerminalError,
)
from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    PublicAction,
    PublicEnvironmentConfig,
    PublicVector2,
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


def test_reset_produces_initial_world_state() -> None:
    """Reset creates a valid initial world state."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(),
        seed=42,
    )

    assert state.step_index == 0
    assert len(state.entities) == 4
    assert len(state.relations) == 3
    assert state.context.width == 100.0
    assert state.context.height == 80.0
    assert state.context.timestep == 1.0


def test_reset_is_reproducible_for_same_seed() -> None:
    """The same configuration and seed produce identical world state."""
    config = make_config()

    first = DeterministicWorld().reset(
        config=config,
        seed=123,
    )

    second = DeterministicWorld().reset(
        config=config,
        seed=123,
    )

    assert first == second


def test_different_seed_can_produce_different_world() -> None:
    """Different seeds are permitted to produce different initial states."""
    config = make_config()

    first = DeterministicWorld().reset(
        config=config,
        seed=123,
    )

    second = DeterministicWorld().reset(
        config=config,
        seed=456,
    )

    assert first != second


def test_entity_identifiers_are_stable() -> None:
    """Entity identifiers are deterministic and stable."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=5),
        seed=42,
    )

    assert [entity.entity_id for entity in state.entities] == [
        "entity-000",
        "entity-001",
        "entity-002",
        "entity-003",
        "entity-004",
    ]


def test_entity_positions_are_within_world_bounds() -> None:
    """Initial positions are generated inside the configured world."""
    config = make_config()

    state = DeterministicWorld().reset(
        config=config,
        seed=42,
    )

    for entity in state.entities:
        assert 0.0 <= entity.position.x <= config.world_width
        assert 0.0 <= entity.position.y <= config.world_height


def test_entity_masses_are_positive() -> None:
    """All generated entities have physically valid positive mass."""
    state = DeterministicWorld().reset(
        config=make_config(),
        seed=42,
    )

    assert all(entity.mass > 0.0 for entity in state.entities)


def test_entity_categories_are_deterministic() -> None:
    """Entity categories follow the deterministic category schedule."""
    state = DeterministicWorld().reset(
        config=make_config(entity_count=6),
        seed=42,
    )

    assert [entity.category.value for entity in state.entities] == [
        "agent",
        "object",
        "landmark",
        "agent",
        "object",
        "landmark",
    ]


def test_relations_reference_existing_entities() -> None:
    """Every relation references entities present in the world."""
    state = DeterministicWorld().reset(
        config=make_config(),
        seed=42,
    )

    entity_ids = {entity.entity_id for entity in state.entities}

    for relation in state.relations:
        assert relation.source_entity_id in entity_ids
        assert relation.target_entity_id in entity_ids


def test_relations_are_deterministic() -> None:
    """Relations are reproduced exactly for identical inputs."""
    config = make_config(entity_count=5)

    first = DeterministicWorld().reset(
        config=config,
        seed=1,
    )

    second = DeterministicWorld().reset(
        config=config,
        seed=1,
    )

    assert first.relations == second.relations


def test_state_requires_reset() -> None:
    """State access before reset is rejected."""
    world = DeterministicWorld()

    with pytest.raises(WorldNotInitializedError, match="must be reset"):
        world.state()


def test_seed_requires_reset() -> None:
    """Seed access before reset is rejected."""
    world = DeterministicWorld()

    with pytest.raises(WorldNotInitializedError, match="must be reset"):
        world.seed()


def test_reset_replaces_previous_world() -> None:
    """A later reset completely replaces the previous simulation state."""
    world = DeterministicWorld()

    first = world.reset(
        config=make_config(entity_count=2),
        seed=1,
    )

    second = world.reset(
        config=make_config(entity_count=5),
        seed=2,
    )

    assert len(first.entities) == 2
    assert len(second.entities) == 5
    assert world.state() == second
    assert world.seed() == 2


def test_zero_entities_are_rejected() -> None:
    """The initial deterministic world requires at least one entity."""
    config = make_config(entity_count=0)

    with pytest.raises(ValueError, match="entity_count"):
        DeterministicWorld().reset(
            config=config,
            seed=42,
        )


def test_no_op_advances_positions_using_existing_velocity() -> None:
    """NO_OP advances position according to the current velocity."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=1),
        seed=42,
    )
    entity_before = before.entities[0]

    after = world.step(
        PublicAction(kind=ActionKind.NO_OP),
    )
    entity_after = after.entities[0]

    assert after.step_index == 1
    assert entity_after.velocity == entity_before.velocity
    assert entity_after.position.x == pytest.approx(
        entity_before.position.x + entity_before.velocity.x
    )
    assert entity_after.position.y == pytest.approx(
        entity_before.position.y + entity_before.velocity.y
    )


def test_move_changes_target_velocity_and_position() -> None:
    """MOVE changes only the selected entity's velocity and position."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    target = before.entities[0]
    other = before.entities[1]

    delta = PublicVector2(x=2.0, y=-0.5)

    after = world.step(
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id=target.entity_id,
            vector=delta,
        )
    )

    updated_target = after.entities[0]
    updated_other = after.entities[1]

    assert updated_target.velocity.x == pytest.approx(
        target.velocity.x + delta.x
    )
    assert updated_target.velocity.y == pytest.approx(
        target.velocity.y + delta.y
    )

    assert updated_target.position.x == pytest.approx(
        target.position.x + updated_target.velocity.x
    )
    assert updated_target.position.y == pytest.approx(
        target.position.y + updated_target.velocity.y
    )

    assert updated_other.velocity == other.velocity
    assert updated_other.position.x == pytest.approx(
        other.position.x + other.velocity.x
    )
    assert updated_other.position.y == pytest.approx(
        other.position.y + other.velocity.y
    )


def test_interact_advances_time_without_changing_physical_state() -> None:
    """INTERACT advances the world without changing physical properties."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    target = before.entities[0]

    after = world.step(
        PublicAction(
            kind=ActionKind.INTERACT,
            entity_id=target.entity_id,
        )
    )

    updated_target = after.entities[0]

    assert after.step_index == 1
    assert updated_target.velocity == target.velocity
    assert updated_target.position.x == pytest.approx(
        target.position.x + target.velocity.x
    )
    assert updated_target.position.y == pytest.approx(
        target.position.y + target.velocity.y
    )


def test_move_requires_entity_id() -> None:
    """MOVE without a target entity is rejected."""
    world = DeterministicWorld()
    world.reset(
        config=make_config(),
        seed=42,
    )

    with pytest.raises(
        InvalidWorldActionError,
        match="entity_id",
    ):
        world.step(
            PublicAction(
                kind=ActionKind.MOVE,
                vector=PublicVector2(x=1.0, y=1.0),
            )
        )


def test_move_requires_vector() -> None:
    """MOVE without a movement vector is rejected."""
    world = DeterministicWorld()
    world.reset(
        config=make_config(),
        seed=42,
    )

    with pytest.raises(
        InvalidWorldActionError,
        match="vector",
    ):
        world.step(
            PublicAction(
                kind=ActionKind.MOVE,
                entity_id="entity-000",
            )
        )


def test_move_rejects_unknown_entity() -> None:
    """MOVE cannot target an unknown entity."""
    world = DeterministicWorld()
    world.reset(
        config=make_config(),
        seed=42,
    )

    with pytest.raises(
        InvalidWorldActionError,
        match="Unknown entity_id",
    ):
        world.step(
            PublicAction(
                kind=ActionKind.MOVE,
                entity_id="entity-999",
                vector=PublicVector2(x=1.0, y=1.0),
            )
        )


def test_interact_requires_entity_id() -> None:
    """INTERACT without a target entity is rejected."""
    world = DeterministicWorld()
    world.reset(
        config=make_config(),
        seed=42,
    )

    with pytest.raises(
        InvalidWorldActionError,
        match="entity_id",
    ):
        world.step(
            PublicAction(kind=ActionKind.INTERACT),
        )


def test_no_op_rejects_entity_id() -> None:
    """NO_OP does not accept an entity target."""
    world = DeterministicWorld()
    world.reset(
        config=make_config(),
        seed=42,
    )

    with pytest.raises(
        InvalidWorldActionError,
        match="entity_id",
    ):
        world.step(
            PublicAction(
                kind=ActionKind.NO_OP,
                entity_id="entity-000",
            )
        )


def test_positions_are_clamped_to_world_bounds() -> None:
    """Transition positions remain inside the configured world."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=1),
        seed=42,
    )

    entity = state.entities[0]

    after = world.step(
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id=entity.entity_id,
            vector=PublicVector2(x=1000.0, y=1000.0),
        )
    )

    updated = after.entities[0]

    assert 0.0 <= updated.position.x <= 100.0
    assert 0.0 <= updated.position.y <= 80.0


def test_world_becomes_terminal_at_max_steps() -> None:
    """The world becomes terminal exactly at max_steps."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(max_steps=2),
        seed=42,
    )

    assert world.is_terminal() is False

    world.step(PublicAction(kind=ActionKind.NO_OP))

    assert world.is_terminal() is False

    world.step(PublicAction(kind=ActionKind.NO_OP))

    assert world.is_terminal() is True


def test_step_after_terminal_is_rejected() -> None:
    """No transition is allowed after terminal state."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(max_steps=1),
        seed=42,
    )

    world.step(PublicAction(kind=ActionKind.NO_OP))

    with pytest.raises(WorldTerminalError, match="already terminal"):
        world.step(PublicAction(kind=ActionKind.NO_OP))


def test_same_action_sequence_is_reproducible() -> None:
    """Identical seeded action sequences produce identical trajectories."""
    config = make_config(entity_count=2)

    first = DeterministicWorld()
    second = DeterministicWorld()

    first.reset(config=config, seed=77)
    second.reset(config=config, seed=77)

    actions = [
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-000",
            vector=PublicVector2(x=0.5, y=-0.25),
        ),
        PublicAction(
            kind=ActionKind.INTERACT,
            entity_id="entity-001",
        ),
        PublicAction(kind=ActionKind.NO_OP),
    ]

    for action in actions:
        assert first.step(action) == second.step(action)