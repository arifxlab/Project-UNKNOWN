"""Internal deterministic world models for Project UNKNOWN.

These models represent simulation state inside the dynamics layer.

Scientific boundary
-------------------
These objects are internal simulation structures. They are not exposed
directly through the public environment API and must not contain hidden
benchmark labels or evaluation records.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EntityCategory(str, Enum):
    """Observable entity categories used by the initial world."""

    AGENT = "agent"
    OBJECT = "object"
    LANDMARK = "landmark"


@dataclass(frozen=True, slots=True)
class Vector2:
    """Two-dimensional vector used by internal world dynamics."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class EntityState:
    """Deterministic internal state for one world entity."""

    entity_id: str
    position: Vector2
    velocity: Vector2
    mass: float
    category: EntityCategory


@dataclass(frozen=True, slots=True)
class RelationState:
    """Deterministic relation between two world entities."""

    relation_id: str
    source_entity_id: str
    target_entity_id: str
    relation_type: str


@dataclass(frozen=True, slots=True)
class WorldContext:
    """Static context describing the current simulation world."""

    width: float
    height: float
    timestep: float


@dataclass(frozen=True, slots=True)
class InterventionRecord:
    """Immutable record of an intervention applied to the world.

    The record is part of internal reproducibility state.

    It contains only intervention input data. It does not contain hidden
    benchmark truth, expected effects, evaluator labels, or outcome
    judgments.
    """

    kind: str
    entity_id: str
    vector: Vector2 | None
    parameters: tuple[tuple[str, object], ...]


@dataclass(frozen=True, slots=True)
class WorldState:
    """Complete deterministic simulation state for one timestep."""

    step_index: int
    entities: tuple[EntityState, ...]
    relations: tuple[RelationState, ...]
    context: WorldContext
    interventions: tuple[InterventionRecord, ...] = ()