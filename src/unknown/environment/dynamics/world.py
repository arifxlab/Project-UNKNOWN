"""Deterministic synthetic world for Project UNKNOWN.

This module implements the initial executable world substrate defined by
the S0.5-A dynamics contract.

The world is intentionally small and deterministic. It provides seeded
initialization and deterministic action transitions. Public observation
projection, interventions, and benchmark conditions are implemented in
later stages.
"""

from __future__ import annotations

import random

from unknown.environment.dynamics.models import (
    EntityCategory,
    EntityState,
    RelationState,
    Vector2,
    WorldContext,
    WorldState,
)
from unknown.environment.schemas.public import (
    ActionKind,
    PublicAction,
    PublicEnvironmentConfig,
)


class DeterministicWorldError(RuntimeError):
    """Base error for deterministic world failures."""


class WorldNotInitializedError(DeterministicWorldError):
    """Raised when the world is used before reset."""


class WorldTerminalError(DeterministicWorldError):
    """Raised when a transition is attempted after termination."""


class InvalidWorldActionError(DeterministicWorldError):
    """Raised when a public action is invalid for the current world."""


class DeterministicWorld:
    """Deterministic internal simulation world.

    The world owns only simulation state. It does not contain benchmark
    truth, evaluation state, discovery logic, or failure-condition labels.
    """

    def __init__(self) -> None:
        self._state: WorldState | None = None
        self._seed: int | None = None
        self._max_steps: int | None = None
        self._allowed_action_kinds: tuple[ActionKind, ...] = ()

    def reset(
        self,
        config: PublicEnvironmentConfig,
        seed: int,
    ) -> WorldState:
        """Reset the world deterministically from configuration and seed."""
        self._validate_config(config)

        rng = random.Random(seed)

        entities = self._create_entities(
            config=config,
            rng=rng,
        )

        context = WorldContext(
            width=config.world_width,
            height=config.world_height,
            timestep=1.0,
        )

        relations = self._create_relations(entities)

        self._state = WorldState(
            step_index=0,
            entities=entities,
            relations=relations,
            context=context,
        )
        self._seed = seed
        self._max_steps = config.max_steps
        self._allowed_action_kinds = tuple(config.allowed_action_kinds)

        return self._state

    def state(self) -> WorldState:
        """Return the current internal world state."""
        if self._state is None:
            raise WorldNotInitializedError(
                "World must be reset before state is requested."
            )

        return self._state

    def seed(self) -> int:
        """Return the seed used for the current world."""
        if self._seed is None:
            raise WorldNotInitializedError(
                "World must be reset before seed is requested."
            )

        return self._seed

    def is_terminal(self) -> bool:
        """Return whether the world has reached its configured horizon."""
        if self._state is None:
            raise WorldNotInitializedError(
                "World must be reset before terminal state is requested."
            )

        if self._max_steps is None:
            raise DeterministicWorldError(
                "World max_steps is unavailable after initialization."
            )

        return self._state.step_index >= self._max_steps

    def step(self, action: PublicAction) -> WorldState:
        """Apply one deterministic action and advance the world."""
        state = self.state()

        if self.is_terminal():
            raise WorldTerminalError(
                "Cannot step a world that is already terminal."
            )

        self._validate_action(action, state)

        next_entities = self._transition_entities(
            state=state,
            action=action,
        )

        self._state = WorldState(
            step_index=state.step_index + 1,
            entities=next_entities,
            relations=state.relations,
            context=state.context,
        )

        return self._state

    def _validate_config(
        self,
        config: PublicEnvironmentConfig,
    ) -> None:
        """Validate configuration required by the deterministic world."""
        if config.max_steps <= 0:
            raise ValueError("max_steps must be greater than zero.")

        if config.world_width <= 0:
            raise ValueError("world_width must be greater than zero.")

        if config.world_height <= 0:
            raise ValueError("world_height must be greater than zero.")

        if config.entity_count <= 0:
            raise ValueError("entity_count must be greater than zero.")

        if config.observation_history_limit <= 0:
            raise ValueError(
                "observation_history_limit must be greater than zero."
            )

        if ActionKind.NO_OP not in config.allowed_action_kinds:
            raise ValueError("NO_OP must be an allowed action.")

    @staticmethod
    def _create_entities(
        config: PublicEnvironmentConfig,
        rng: random.Random,
    ) -> tuple[EntityState, ...]:
        """Create deterministic entities from a seeded generator."""
        categories = (
            EntityCategory.AGENT,
            EntityCategory.OBJECT,
            EntityCategory.LANDMARK,
        )

        entities: list[EntityState] = []

        for index in range(config.entity_count):
            position = Vector2(
                x=rng.uniform(0.0, config.world_width),
                y=rng.uniform(0.0, config.world_height),
            )

            velocity = Vector2(
                x=rng.uniform(-1.0, 1.0),
                y=rng.uniform(-1.0, 1.0),
            )

            mass = float(rng.randint(1, 10))

            category = categories[index % len(categories)]

            entities.append(
                EntityState(
                    entity_id=f"entity-{index:03d}",
                    position=position,
                    velocity=velocity,
                    mass=mass,
                    category=category,
                )
            )

        return tuple(entities)

    @staticmethod
    def _create_relations(
        entities: tuple[EntityState, ...],
    ) -> tuple[RelationState, ...]:
        """Create deterministic relations from stable entity ordering."""
        if len(entities) < 2:
            return ()

        relations: list[RelationState] = []

        for index in range(len(entities) - 1):
            source = entities[index]
            target = entities[index + 1]

            relations.append(
                RelationState(
                    relation_id=f"relation-{index:03d}",
                    source_entity_id=source.entity_id,
                    target_entity_id=target.entity_id,
                    relation_type="adjacent",
                )
            )

        return tuple(relations)

    def _validate_action(
        self,
        action: PublicAction,
        state: WorldState,
    ) -> None:
        """Validate an action against world state and configuration."""
        if action.kind not in self._allowed_action_kinds:
            raise InvalidWorldActionError(
                f"Action kind {action.kind!r} is not allowed by the "
                "current environment configuration."
            )

        entity_ids = {entity.entity_id for entity in state.entities}

        if action.kind is ActionKind.NO_OP:
            if action.entity_id is not None:
                raise InvalidWorldActionError(
                    "NO_OP actions must not specify an entity_id."
                )

            if action.vector is not None:
                raise InvalidWorldActionError(
                    "NO_OP actions must not specify a vector."
                )

            return

        if action.kind is ActionKind.MOVE:
            if action.entity_id is None:
                raise InvalidWorldActionError(
                    "MOVE actions require an entity_id."
                )

            if action.entity_id not in entity_ids:
                raise InvalidWorldActionError(
                    f"Unknown entity_id: {action.entity_id!r}."
                )

            if action.vector is None:
                raise InvalidWorldActionError(
                    "MOVE actions require a vector."
                )

            return

        if action.kind is ActionKind.INTERACT:
            if action.entity_id is None:
                raise InvalidWorldActionError(
                    "INTERACT actions require an entity_id."
                )

            if action.entity_id not in entity_ids:
                raise InvalidWorldActionError(
                    f"Unknown entity_id: {action.entity_id!r}."
                )

            return

        raise InvalidWorldActionError(
            f"Unsupported action kind: {action.kind!r}."
        )

    @classmethod
    def _transition_entities(
        cls,
        state: WorldState,
        action: PublicAction,
    ) -> tuple[EntityState, ...]:
        """Compute the next entity states deterministically."""
        updated: list[EntityState] = []

        for entity in state.entities:
            velocity = entity.velocity

            if (
                action.kind is ActionKind.MOVE
                and action.entity_id == entity.entity_id
            ):
                assert action.vector is not None

                velocity = Vector2(
                    x=entity.velocity.x + action.vector.x,
                    y=entity.velocity.y + action.vector.y,
                )

            position = Vector2(
                x=entity.position.x
                + velocity.x * state.context.timestep,
                y=entity.position.y
                + velocity.y * state.context.timestep,
            )

            position = cls._clamp_position(
                position=position,
                context=state.context,
            )

            updated.append(
                EntityState(
                    entity_id=entity.entity_id,
                    position=position,
                    velocity=velocity,
                    mass=entity.mass,
                    category=entity.category,
                )
            )

        return tuple(updated)

    @staticmethod
    def _clamp_position(
        position: Vector2,
        context: WorldContext,
    ) -> Vector2:
        """Keep an entity position inside the world bounds."""
        return Vector2(
            x=min(max(position.x, 0.0), context.width),
            y=min(max(position.y, 0.0), context.height),
        )