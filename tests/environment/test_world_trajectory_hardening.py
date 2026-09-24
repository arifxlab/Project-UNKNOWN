"""Hardening tests for authoritative world trajectories."""

from __future__ import annotations

import math

import pytest

from unknown.environment.dynamics import (
    DeterministicWorld,
    InvalidWorldActionError,
)
from unknown.environment.schemas.public import (
    ActionKind,
    PublicAction,
    PublicVector2,
)

from tests.helpers.environment import make_config


def test_long_action_sequence_is_bitwise_reproducible() -> None:
    """A fixed seed and fixed action sequence reproduce every state."""
    config = make_config(entity_count=3, max_steps=8)

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
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-002",
            vector=PublicVector2(x=-0.75, y=0.5),
        ),
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-000",
            vector=PublicVector2(x=0.25, y=0.25),
        ),
        PublicAction(
            kind=ActionKind.INTERACT,
            entity_id="entity-002",
        ),
        PublicAction(kind=ActionKind.NO_OP),
    ]

    first = DeterministicWorld()
    second = DeterministicWorld()

    first.reset(config=config, seed=314159)
    second.reset(config=config, seed=314159)

    assert first.state() == second.state()

    for action in actions:
        first_state = first.step(action)
        second_state = second.step(action)

        assert first_state == second_state


def test_invalid_action_does_not_mutate_state() -> None:
    """Rejecting an invalid action leaves the authoritative state unchanged."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=2),
        seed=42,
    )

    before = world.state()

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

    after = world.state()

    assert after == before
    assert world.is_terminal() is False


def test_non_finite_move_vector_is_rejected() -> None:
    """Non-finite movement values cannot enter the simulation."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=1),
        seed=42,
    )

    invalid_vectors = (
        PublicVector2(x=math.nan, y=0.0),
        PublicVector2(x=0.0, y=math.nan),
        PublicVector2(x=math.inf, y=0.0),
        PublicVector2(x=0.0, y=-math.inf),
    )

    for vector in invalid_vectors:
        with pytest.raises(
            InvalidWorldActionError,
            match="must be finite",
        ):
            world.step(
                PublicAction(
                    kind=ActionKind.MOVE,
                    entity_id="entity-000",
                    vector=vector,
                )
            )


def test_non_finite_move_vector_does_not_mutate_state() -> None:
    """Rejecting non-finite input leaves the world unchanged."""
    world = DeterministicWorld()

    world.reset(
        config=make_config(entity_count=1),
        seed=42,
    )

    before = world.state()

    with pytest.raises(
        InvalidWorldActionError,
        match="must be finite",
    ):
        world.step(
            PublicAction(
                kind=ActionKind.MOVE,
                entity_id="entity-000",
                vector=PublicVector2(x=math.nan, y=0.0),
            )
        )

    assert world.state() == before


def test_trajectory_preserves_entity_identity_and_mass() -> None:
    """Ordinary transitions preserve identity, mass, and category."""
    config = make_config(entity_count=4, max_steps=5)

    world = DeterministicWorld()

    initial = world.reset(
        config=config,
        seed=99,
    )

    initial_properties = {
        entity.entity_id: (entity.mass, entity.category)
        for entity in initial.entities
    }

    actions = [
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-001",
            vector=PublicVector2(x=3.0, y=-2.0),
        ),
        PublicAction(
            kind=ActionKind.INTERACT,
            entity_id="entity-002",
        ),
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-003",
            vector=PublicVector2(x=-1.0, y=4.0),
        ),
    ]

    for action in actions:
        state = world.step(action)

        for entity in state.entities:
            expected_mass, expected_category = initial_properties[
                entity.entity_id
            ]

            assert entity.mass == expected_mass
            assert entity.category == expected_category


def test_trajectory_preserves_position_bounds() -> None:
    """Every state in a trajectory remains inside world bounds."""
    config = make_config(entity_count=4, max_steps=6)

    world = DeterministicWorld()

    world.reset(
        config=config,
        seed=12345,
    )

    actions = [
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-000",
            vector=PublicVector2(x=1000.0, y=-1000.0),
        ),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-001",
            vector=PublicVector2(x=-1000.0, y=1000.0),
        ),
        PublicAction(kind=ActionKind.NO_OP),
        PublicAction(
            kind=ActionKind.MOVE,
            entity_id="entity-002",
            vector=PublicVector2(x=500.0, y=500.0),
        ),
        PublicAction(kind=ActionKind.NO_OP),
    ]

    for action in actions:
        state = world.step(action)

        for entity in state.entities:
            assert 0.0 <= entity.position.x <= config.world_width
            assert 0.0 <= entity.position.y <= config.world_height


def test_reset_after_terminal_creates_new_trajectory() -> None:
    """Reset fully replaces a terminal world with a fresh deterministic run."""
    config = make_config(entity_count=2, max_steps=1)

    world = DeterministicWorld()

    first = world.reset(config=config, seed=42)
    terminal = world.step(PublicAction(kind=ActionKind.NO_OP))

    assert terminal.step_index == 1
    assert world.is_terminal() is True

    second = world.reset(config=config, seed=42)

    assert second.step_index == 0
    assert world.is_terminal() is False
    assert second == first

def test_boolean_max_steps_is_rejected() -> None:
    """Boolean max_steps must not be accepted as an integer horizon."""
    config = make_config(max_steps=True)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="max_steps must be an integer"):
        DeterministicWorld().reset(
            config=config,
            seed=42,
        )


def test_boolean_entity_count_is_rejected() -> None:
    """Boolean entity_count must not be accepted as an integer count."""
    config = make_config(entity_count=True)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="entity_count must be an integer"):
        DeterministicWorld().reset(
            config=config,
            seed=42,
        )