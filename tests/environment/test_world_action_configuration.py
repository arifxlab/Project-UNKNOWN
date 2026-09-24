"""Tests for deterministic-world action configuration enforcement."""

from __future__ import annotations

import pytest

from unknown.environment.dynamics import (
    DeterministicWorld,
    InvalidWorldActionError,
    Vector2,
)
from unknown.environment.schemas.public import (
    ActionKind,
    PublicAction,
)

from tests.helpers.environment import make_config


def test_move_is_rejected_when_not_allowed() -> None:
    config = make_config(
        allowed_action_kinds=(ActionKind.NO_OP,),
    )

    world = DeterministicWorld()
    state = world.reset(config=config, seed=42)

    action = PublicAction(
        kind=ActionKind.MOVE,
        entity_id=state.entities[0].entity_id,
        vector=Vector2(x=1.0, y=0.0),
    )

    with pytest.raises(InvalidWorldActionError, match="not allowed"):
        world.step(action)


def test_interact_is_rejected_when_not_allowed() -> None:
    config = make_config(
        allowed_action_kinds=(ActionKind.NO_OP, ActionKind.MOVE),
    )

    world = DeterministicWorld()
    state = world.reset(config=config, seed=42)

    action = PublicAction(
        kind=ActionKind.INTERACT,
        entity_id=state.entities[0].entity_id,
    )

    with pytest.raises(InvalidWorldActionError, match="not allowed"):
        world.step(action)


def test_allowed_move_remains_executable() -> None:
    config = make_config(
        allowed_action_kinds=(ActionKind.NO_OP, ActionKind.MOVE),
    )

    world = DeterministicWorld()
    state = world.reset(config=config, seed=42)

    action = PublicAction(
        kind=ActionKind.MOVE,
        entity_id=state.entities[0].entity_id,
        vector=Vector2(x=1.0, y=0.0),
    )

    next_state = world.step(action)

    assert next_state.step_index == 1