"""Invariant tests for the authoritative deterministic world."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from tests.helpers.environment import make_config
from unknown.environment.dynamics import DeterministicWorld
from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    PublicAction,
    PublicIntervention,
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


def test_intervention_collection_is_immutable() -> None:
    """Intervention history is represented as an immutable tuple."""
    world = DeterministicWorld()

    state = world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    assert isinstance(state.interventions, tuple)


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
        assert after.interventions == before.interventions
        before = after


def test_set_position_preserves_velocity_and_relations() -> None:
    """SET_POSITION changes only target position and transition history."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=3),
        seed=42,
    )

    target_id = "entity-001"
    target_before = next(
        entity for entity in before.entities
        if entity.entity_id == target_id
    )

    after = world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id=target_id,
            vector=PublicVector2(x=25.0, y=35.0),
        )
    )

    target_after = next(
        entity for entity in after.entities
        if entity.entity_id == target_id
    )

    assert target_after.position == type(target_after.position)(
        x=25.0,
        y=35.0,
    )
    assert target_after.velocity == target_before.velocity
    assert target_after.mass == target_before.mass
    assert target_after.category == target_before.category
    assert after.relations == before.relations


def test_set_velocity_preserves_position_and_relations() -> None:
    """SET_VELOCITY changes only target velocity and transition history."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=3),
        seed=42,
    )

    target_id = "entity-001"
    target_before = next(
        entity for entity in before.entities
        if entity.entity_id == target_id
    )

    after = world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_VELOCITY,
            entity_id=target_id,
            vector=PublicVector2(x=-5.0, y=6.0),
        )
    )

    target_after = next(
        entity for entity in after.entities
        if entity.entity_id == target_id
    )

    assert target_after.position == target_before.position
    assert target_after.velocity == type(target_after.velocity)(
        x=-5.0,
        y=6.0,
    )
    assert target_after.mass == target_before.mass
    assert target_after.category == target_before.category
    assert after.relations == before.relations


def test_remove_entity_removes_only_incident_relations() -> None:
    """REMOVE_ENTITY removes the target and its incident relations only."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=4),
        seed=42,
    )

    target_id = "entity-001"

    after = world.intervene(
        PublicIntervention(
            kind=InterventionKind.REMOVE_ENTITY,
            entity_id=target_id,
        )
    )

    remaining_ids = {
        entity.entity_id
        for entity in after.entities
    }

    assert target_id not in remaining_ids
    assert len(after.entities) == len(before.entities) - 1

    assert all(
        relation.source_entity_id != target_id
        and relation.target_entity_id != target_id
        for relation in after.relations
    )

    assert len(after.relations) == 1
    assert (
        after.relations[0].source_entity_id == "entity-002"
        and after.relations[0].target_entity_id == "entity-003"
    )


def test_intervention_advances_step_without_ordinary_kinematics() -> None:
    """Interventions advance time but do not execute ordinary movement."""
    world = DeterministicWorld()

    before = world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    target_id = "entity-000"
    target_before = before.entities[0]

    after = world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_VELOCITY,
            entity_id=target_id,
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    target_after = after.entities[0]

    assert after.step_index == before.step_index + 1
    assert target_after.position == target_before.position