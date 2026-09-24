"""Dedicated tests for authoritative deterministic interventions."""

from __future__ import annotations

import math

import pytest

from tests.helpers.environment import make_config
from unknown.environment.dynamics import (
    DeterministicWorld,
    InvalidWorldInterventionError,
    WorldTerminalError,
)
from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    PublicAction,
    PublicIntervention,
    PublicVector2,
)


def test_intervention_is_recorded_in_reproducibility_state() -> None:
    """Applied interventions must become part of WorldState."""
    world = DeterministicWorld()

    initial = world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    assert initial.interventions == ()

    state = world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id="entity-000",
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    assert len(state.interventions) == 1

    record = state.interventions[0]

    assert record.kind == InterventionKind.SET_POSITION.value
    assert record.entity_id == "entity-000"
    assert record.vector is not None
    assert record.vector.x == 10.0
    assert record.vector.y == 20.0


def test_multiple_interventions_preserve_order() -> None:
    """Intervention history preserves exact transition order."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=2, max_steps=4),
        seed=42,
    )

    world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id="entity-000",
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_VELOCITY,
            entity_id="entity-001",
            vector=PublicVector2(x=3.0, y=4.0),
        )
    )

    history = world.state().interventions

    assert [record.kind for record in history] == [
        InterventionKind.SET_POSITION.value,
        InterventionKind.SET_VELOCITY.value,
    ]

    assert [record.entity_id for record in history] == [
        "entity-000",
        "entity-001",
    ]


def test_action_and_intervention_sequence_is_reproducible() -> None:
    """Mixed ordinary/intervention trajectories must be deterministic."""
    config = make_config(entity_count=3, max_steps=7)

    first = DeterministicWorld()
    second = DeterministicWorld()

    first.reset(config=config, seed=1234)
    second.reset(config=config, seed=1234)

    transitions = [
        (
            "action",
            PublicAction(kind=ActionKind.NO_OP),
        ),
        (
            "intervention",
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-001",
                vector=PublicVector2(x=20.0, y=30.0),
            ),
        ),
        (
            "action",
            PublicAction(
                kind=ActionKind.MOVE,
                entity_id="entity-000",
                vector=PublicVector2(x=1.0, y=-2.0),
            ),
        ),
        (
            "intervention",
            PublicIntervention(
                kind=InterventionKind.SET_VELOCITY,
                entity_id="entity-002",
                vector=PublicVector2(x=4.0, y=-3.0),
            ),
        ),
        (
            "action",
            PublicAction(kind=ActionKind.INTERACT, entity_id="entity-002"),
        ),
        (
            "intervention",
            PublicIntervention(
                kind=InterventionKind.REMOVE_ENTITY,
                entity_id="entity-001",
            ),
        ),
        (
            "action",
            PublicAction(kind=ActionKind.NO_OP),
        ),
    ]

    for transition_kind, transition in transitions:
        if transition_kind == "action":
            first_state = first.step(transition)
            second_state = second.step(transition)
        else:
            first_state = first.intervene(transition)
            second_state = second.intervene(transition)

        assert first_state == second_state


def test_invalid_intervention_does_not_mutate_world() -> None:
    """All rejected interventions must leave state unchanged."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    before = world.state()

    with pytest.raises(
        InvalidWorldInterventionError,
        match="Unknown entity_id",
    ):
        world.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-999",
                vector=PublicVector2(x=10.0, y=20.0),
            )
        )

    assert world.state() == before


@pytest.mark.parametrize(
    "vector",
    [
        PublicVector2(x=math.nan, y=0.0),
        PublicVector2(x=0.0, y=math.nan),
        PublicVector2(x=math.inf, y=0.0),
        PublicVector2(x=0.0, y=-math.inf),
    ],
)
def test_set_velocity_rejects_non_finite_vector(
    vector: PublicVector2,
) -> None:
    """SET_VELOCITY must reject non-finite values."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=1),
        seed=42,
    )

    before = world.state()

    with pytest.raises(
        InvalidWorldInterventionError,
        match="must be finite",
    ):
        world.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_VELOCITY,
                entity_id="entity-000",
                vector=vector,
            )
        )

    assert world.state() == before


def test_set_position_rejects_out_of_bounds_vector() -> None:
    """SET_POSITION must reject rather than clamp intervention input."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(
            entity_count=1,
            world_width=100.0,
            world_height=100.0,
        ),
        seed=42,
    )

    before = world.state()

    with pytest.raises(
        InvalidWorldInterventionError,
        match="inside world bounds",
    ):
        world.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-000",
                vector=PublicVector2(x=101.0, y=50.0),
            )
        )

    assert world.state() == before


def test_remove_entity_rejects_unknown_entity() -> None:
    """REMOVE_ENTITY must reject missing entity identifiers."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    before = world.state()

    with pytest.raises(
        InvalidWorldInterventionError,
        match="Unknown entity_id",
    ):
        world.intervene(
            PublicIntervention(
                kind=InterventionKind.REMOVE_ENTITY,
                entity_id="entity-999",
            )
        )

    assert world.state() == before


def test_intervention_after_terminal_state_is_rejected() -> None:
    """Terminal worlds cannot accept interventions."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=1, max_steps=1),
        seed=42,
    )

    world.step(PublicAction(kind=ActionKind.NO_OP))

    before = world.state()

    with pytest.raises(WorldTerminalError):
        world.intervene(
            PublicIntervention(
                kind=InterventionKind.SET_POSITION,
                entity_id="entity-000",
                vector=PublicVector2(x=10.0, y=20.0),
            )
        )

    assert world.state() == before


def test_intervention_history_is_reset_with_new_episode() -> None:
    """Reset must discard intervention history from the prior episode."""
    world = DeterministicWorld()

    config = make_config(entity_count=1, max_steps=3)

    first = world.reset(config=config, seed=42)

    world.intervene(
        PublicIntervention(
            kind=InterventionKind.SET_POSITION,
            entity_id="entity-000",
            vector=PublicVector2(x=10.0, y=20.0),
        )
    )

    assert len(world.state().interventions) == 1

    second = world.reset(config=config, seed=42)

    assert second == first
    assert second.interventions == ()