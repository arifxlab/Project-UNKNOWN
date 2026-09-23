"""Tests for the public observation projection."""

from __future__ import annotations

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
from unknown.environment.schemas.public import ObservationKind


def make_world_state() -> WorldState:
    """Create a representative internal world state."""

    return WorldState(
        step_index=7,
        entities=(
            EntityState(
                entity_id="entity-0000",
                position=Vector2(10.0, 20.0),
                velocity=Vector2(1.5, -2.0),
                mass=8.5,
                category=EntityCategory.AGENT,
            ),
            EntityState(
                entity_id="entity-0001",
                position=Vector2(30.0, 40.0),
                velocity=Vector2(-1.0, 0.5),
                mass=25.0,
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


def test_projection_preserves_public_entity_identity_position_and_velocity() -> None:
    """Public entities contain the primitive observable quantities."""

    observation = PublicObservationProjector().project(make_world_state())

    assert len(observation.entities) == 2

    first = observation.entities[0]

    assert first.entity_id == "entity-0000"
    assert first.position.x == 10.0
    assert first.position.y == 20.0
    assert first.velocity.x == 1.5
    assert first.velocity.y == -2.0


def test_projection_does_not_expose_internal_mass_or_category() -> None:
    """Internal-only physical and semantic fields do not cross the boundary."""

    observation = PublicObservationProjector().project(make_world_state())

    first = observation.entities[0]

    assert first.attributes == {}

    public_text = repr(first)

    assert "mass" not in public_text
    assert "category" not in public_text
    assert "8.5" not in public_text
    assert "AGENT" not in public_text


def test_projection_preserves_public_relations() -> None:
    """Explicitly public relations are projected without hidden metadata."""

    observation = PublicObservationProjector().project(make_world_state())

    assert len(observation.relations) == 1

    relation = observation.relations[0]

    assert relation.relation_id == "relation-0000"
    assert relation.source_entity_id == "entity-0000"
    assert relation.target_entity_id == "entity-0001"
    assert relation.relation_type == "adjacent"
    assert relation.value is None


def test_projection_preserves_public_events() -> None:
    """Explicit public events are included unchanged."""

    observation = PublicObservationProjector().project(
        make_world_state(),
        events=("entity_moved", "interaction_available"),
    )

    assert observation.events == (
        "entity_moved",
        "interaction_available",
    )


def test_projection_sets_state_observation_kind() -> None:
    """World-state projection produces a state observation."""

    observation = PublicObservationProjector().project(make_world_state())

    assert observation.kind is ObservationKind.STATE


def test_projection_uses_step_index() -> None:
    """The public step index matches the internal simulation step."""

    observation = PublicObservationProjector().project(make_world_state())

    assert observation.step_index == 7


def test_projection_uses_deterministic_timestamp() -> None:
    """Timestamp is simulation time rather than wall-clock time."""

    observation = PublicObservationProjector().project(make_world_state())

    assert observation.timestamp == 7


def test_projection_generates_deterministic_observation_identifier() -> None:
    """Observation identifiers are deterministic."""

    observation = PublicObservationProjector().project(make_world_state())

    assert observation.observation_id == "observation-00000007"


def test_projection_preserves_entity_order() -> None:
    """Entity ordering is deterministic and follows world-state ordering."""

    observation = PublicObservationProjector().project(make_world_state())

    assert tuple(entity.entity_id for entity in observation.entities) == (
        "entity-0000",
        "entity-0001",
    )


def test_projection_preserves_relation_order() -> None:
    """Relation ordering is deterministic and follows world-state ordering."""

    observation = PublicObservationProjector().project(make_world_state())

    assert tuple(relation.relation_id for relation in observation.relations) == (
        "relation-0000",
    )