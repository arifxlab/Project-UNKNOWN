"""Determinism and purity tests for public observation projection."""

from __future__ import annotations

from dataclasses import replace

from unknown.environment.dynamics.models import (
    EntityCategory,
    EntityState,
    RelationState,
    Vector2,
    WorldContext,
    WorldState,
)
from unknown.environment.observation.projection import (
    PublicObservationProjector,
)


def make_world_state() -> WorldState:
    """Create a deterministic world state."""

    return WorldState(
        step_index=12,
        entities=(
            EntityState(
                entity_id="entity-0000",
                position=Vector2(12.0, 18.0),
                velocity=Vector2(1.0, 2.0),
                mass=4.0,
                category=EntityCategory.AGENT,
            ),
            EntityState(
                entity_id="entity-0001",
                position=Vector2(50.0, 60.0),
                velocity=Vector2(-2.0, 0.5),
                mass=12.0,
                category=EntityCategory.OBJECT,
            ),
        ),
        relations=(
            RelationState(
                relation_id="relation-0000",
                source_entity_id="entity-0000",
                target_entity_id="entity-0001",
                relation_type="adjacent",
            ),
        ),
        context=WorldContext(
            width=100.0,
            height=100.0,
            timestep=1.0,
        ),
    )


def test_same_state_produces_identical_observations() -> None:
    """Repeated projection of the same state is deterministic."""

    projector = PublicObservationProjector()
    world = make_world_state()

    first = projector.project(
        world,
        events=("event_a",),
    )
    second = projector.project(
        world,
        events=("event_a",),
    )

    assert first == second


def test_projection_does_not_mutate_world_state() -> None:
    """Projection is observationally pure."""

    projector = PublicObservationProjector()
    world = make_world_state()

    original = world

    projector.project(
        world,
        events=("event_a", "event_b"),
    )

    assert world == original


def test_different_step_indices_produce_different_observation_ids() -> None:
    """Observation identifiers track simulation position deterministically."""

    projector = PublicObservationProjector()

    first = projector.project(make_world_state())

    later_world = replace(
        make_world_state(),
        step_index=13,
    )

    second = projector.project(later_world)

    assert first.observation_id != second.observation_id
    assert first.observation_id == "observation-00000012"
    assert second.observation_id == "observation-00000013"


def test_different_public_events_change_only_public_events() -> None:
    """Changing explicit events does not alter projected world state."""

    projector = PublicObservationProjector()
    world = make_world_state()

    first = projector.project(
        world,
        events=("event_a",),
    )
    second = projector.project(
        world,
        events=("event_b",),
    )

    assert first.entities == second.entities
    assert first.relations == second.relations
    assert first.step_index == second.step_index
    assert first.timestamp == second.timestamp
    assert first.observation_id == second.observation_id
    assert first.events != second.events


def test_internal_mass_changes_do_not_change_public_observation() -> None:
    """Internal mass is irrelevant to the current public projection."""

    projector = PublicObservationProjector()

    world = make_world_state()

    changed_entity = replace(
        world.entities[0],
        mass=9999.0,
    )

    changed_world = replace(
        world,
        entities=(changed_entity, world.entities[1]),
    )

    first = projector.project(world)
    second = projector.project(changed_world)

    assert first == second


def test_internal_category_changes_do_not_change_public_observation() -> None:
    """Internal semantic category is not exposed by projection."""

    projector = PublicObservationProjector()

    world = make_world_state()

    changed_entity = replace(
        world.entities[0],
        category=EntityCategory.LANDMARK,
    )

    changed_world = replace(
        world,
        entities=(changed_entity, world.entities[1]),
    )

    first = projector.project(world)
    second = projector.project(changed_world)

    assert first == second