"""Invariant tests for the authoritative deterministic world."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from tests.helpers.environment import make_config
from unknown.environment.dynamics import DeterministicWorld
from unknown.environment.schemas.public import (
    ActionKind,
    PublicAction,
    PublicVector2,
)


def test_world_state_is_immutable() -> None:
    """Returned world state cannot be mutated in place."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    with pytest.raises(FrozenInstanceError):
        state.step_index = 99  # type: ignore[misc]


def test_entity_state_is_immutable() -> None:
    """Returned entity state cannot be mutated in place."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=1),
        seed=42,
    )

    with pytest.raises(FrozenInstanceError):
        state.entities[0].mass = 999.0  # type: ignore[misc]


def test_relation_collection_is_immutable() -> None:
    """Relations are returned as an immutable tuple."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=3),
        seed=42,
    )

    assert isinstance(state.relations, tuple)

    with pytest.raises(AttributeError):
        state.relations.append(state.relations[0])  # type: ignore[attr-defined]


def test_entity_collection_is_immutable() -> None:
    """Entities are returned as an immutable tuple."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=3),
        seed=42,
    )

    assert isinstance(state.entities, tuple)

    with pytest.raises(AttributeError):
        state.entities.append(state.entities[0])  # type: ignore[attr-defined]


def test_no_op_preserves_velocity_for_every_entity() -> None:
    """NO_OP never changes entity velocity."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=5),
        seed=7,
    )

    after = world.step(
        PublicAction(kind=ActionKind.NO_OP),
    )

    before_velocities = {
        entity.entity_id: entity.velocity
        for entity in before.entities
    }

    for entity in after.entities:
        assert entity.velocity == before_velocities[entity.entity_id]


def test_move_changes_only_target_velocity() -> None:
    """MOVE modifies velocity only for its selected entity."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=4),
        seed=7,
    )

    target_id = "entity-002"

    after = world.step(
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id=target_id,
            vector=PublicVector2(x=2.0, y=-3.0),
        )
    )

    before_velocities = {
        entity.entity_id: entity.velocity
        for entity in before.entities
    }

    for entity in after.entities:
        if entity.entity_id == target_id:
            assert entity.velocity.x == pytest.approx(
                before_velocities[target_id].x + 2.0
            )
            assert entity.velocity.y == pytest.approx(
                before_velocities[target_id].y - 3.0
            )
        else:
            assert entity.velocity == before_velocities[entity.entity_id]


def test_relations_remain_stable_during_ordinary_actions() -> None:
    """Ordinary actions do not silently rewrite relations."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=5),
        seed=7,
    )

    actions = [
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-000",
            vector=PublicVector2(x=1.0, y=2.0),
        ),
        PublicAction(
            kind=ActionKind.INTERACT,
            entity_id="entity-003",
        ),
    ]

    for action in actions:
        after = world.step(action)
        assert after.relations == before.relations
        before = after