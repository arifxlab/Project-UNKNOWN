"""Boundary and leakage tests for public observation projection."""

from __future__ import annotations

from dataclasses import fields

from unknown.environment.dynamics.models import (
    EntityCategory,
    EntityState,
    RelationState,
    Vector2,
    WorldContext,
    WorldState,
)
from unknown.environment.observation.projection import (
    ObservationProjectionError,
    PublicObservationProjector,
)


def make_world_state() -> WorldState:
    """Create a world state containing internal-only information."""

    return WorldState(
        step_index=3,
        entities=(
            EntityState(
                entity_id="entity-0000",
                position=Vector2(5.0, 10.0),
                velocity=Vector2(2.0, 3.0),
                mass=100.0,
                category=EntityCategory.LANDMARK,
            ),
        ),
        relations=(
            RelationState(
                relation_id="relation-0000",
                source_entity_id="entity-0000",
                target_entity_id="entity-0000",
                relation_type="self",
            ),
        ),
        context=WorldContext(
            width=100.0,
            height=100.0,
            timestep=0.5,
        ),
    )


def test_public_entity_contains_only_contract_fields() -> None:
    """The projected entity schema contains no internal state fields."""

    observation = PublicObservationProjector().project(make_world_state())

    public_entity = observation.entities[0]

    field_names = {
        field.name
        for field in fields(public_entity)
    }

    assert field_names == {
        "entity_id",
        "position",
        "velocity",
        "attributes",
    }


def test_projection_does_not_expose_internal_mass_or_category() -> None:
    """Internal-only physical and semantic fields do not cross the boundary."""

    observation = PublicObservationProjector().project(make_world_state())

    first = observation.entities[0]

    assert first.attributes == {}

    public_text = repr(first)

    assert "mass" not in public_text
    assert "category" not in public_text
    assert "100.0" not in public_text
    assert "LANDMARK" not in public_text


def test_projection_does_not_derive_speed() -> None:
    """Speed is not silently promoted into the primitive observation."""

    observation = PublicObservationProjector().project(make_world_state())

    public_entity = observation.entities[0]

    assert "speed" not in public_entity.attributes
    assert "magnitude" not in public_entity.attributes


def test_projection_does_not_derive_position_or_velocity_relations() -> None:
    """Derived relative quantities are not injected into attributes."""

    observation = PublicObservationProjector().project(make_world_state())

    public_entity = observation.entities[0]

    assert "distance" not in public_entity.attributes
    assert "relative_position" not in public_entity.attributes
    assert "relative_velocity" not in public_entity.attributes
    assert "nearest_entity" not in public_entity.attributes


def test_projection_does_not_expose_world_context() -> None:
    """Internal world configuration is not copied into public entities."""

    observation = PublicObservationProjector().project(make_world_state())

    public_entity = observation.entities[0]

    assert "width" not in public_entity.attributes
    assert "height" not in public_entity.attributes
    assert "timestep" not in public_entity.attributes


def test_projection_rejects_invalid_world_state_type() -> None:
    """Projection refuses objects outside the dynamics contract."""

    projector = PublicObservationProjector()

    try:
        projector.project(object())  # type: ignore[arg-type]
    except ObservationProjectionError as error:
        assert "WorldState" in str(error)
    else:
        raise AssertionError("Expected ObservationProjectionError.")


def test_projection_rejects_duplicate_entity_ids() -> None:
    """Duplicate public identifiers cannot create ambiguous observations."""

    world = make_world_state()

    duplicate = EntityState(
        entity_id="entity-0000",
        position=Vector2(20.0, 20.0),
        velocity=Vector2(0.0, 0.0),
        mass=1.0,
        category=EntityCategory.OBJECT,
    )

    invalid_world = WorldState(
        step_index=world.step_index,
        entities=world.entities + (duplicate,),
        relations=world.relations,
        context=world.context,
    )

    try:
        PublicObservationProjector().project(invalid_world)
    except ObservationProjectionError as error:
        assert "duplicate entity" in str(error)
    else:
        raise AssertionError("Expected ObservationProjectionError.")


def test_projection_rejects_relation_with_unknown_entity() -> None:
    """Relations cannot leak or fabricate identifiers outside the world."""

    world = make_world_state()

    invalid_relation = RelationState(
        relation_id="relation-invalid",
        source_entity_id="entity-0000",
        target_entity_id="entity-9999",
        relation_type="adjacent",
    )

    invalid_world = WorldState(
        step_index=world.step_index,
        entities=world.entities,
        relations=(invalid_relation,),
        context=world.context,
    )

    try:
        PublicObservationProjector().project(invalid_world)
    except ObservationProjectionError as error:
        assert "unknown target" in str(error)
    else:
        raise AssertionError("Expected ObservationProjectionError.")


def test_projection_rejects_string_as_event_sequence() -> None:
    """A single string must not be interpreted as many public events."""

    try:
        PublicObservationProjector().project(
            make_world_state(),
            events="hidden_condition",  # type: ignore[arg-type]
        )
    except ObservationProjectionError as error:
        assert "sequence of event strings" in str(error)
    else:
        raise AssertionError("Expected ObservationProjectionError.")