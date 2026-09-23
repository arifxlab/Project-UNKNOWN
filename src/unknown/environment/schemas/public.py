"""Public environment schemas for Project UNKNOWN.

These schemas define information that is legitimately available to the
UNKNOWN discovery system.

Scientific boundary
-------------------
Objects in this module must contain only public experiment information.

They must not contain:

- hidden state
- ground-truth representations
- benchmark condition labels
- evaluation labels
- oracle outcomes
- hidden causal structure
- evaluation scores

The public schemas are intentionally independent from the hidden and
evaluation schemas.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class ObservationKind(str, Enum):
    """Kinds of public observations supported by the environment."""

    STATE = "state"
    EVENT = "event"


class ActionKind(str, Enum):
    """Kinds of actions available through the public environment."""

    NO_OP = "no_op"
    MOVE = "move"
    INTERACT = "interact"


class InterventionKind(str, Enum):
    """Kinds of interventions available through the public interface."""

    SET_POSITION = "set_position"
    SET_VELOCITY = "set_velocity"
    REMOVE_ENTITY = "remove_entity"


@dataclass(frozen=True, slots=True)
class PublicVector2:
    """Two-dimensional public vector."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class PublicEntity:
    """Publicly observable entity.

    The identifier is intentionally opaque and carries no semantic meaning.
    """

    entity_id: str
    position: PublicVector2
    velocity: PublicVector2
    attributes: Mapping[str, str | int | float | bool]


@dataclass(frozen=True, slots=True)
class PublicRelation:
    """A publicly observable relation between entities."""

    relation_id: str
    source_entity_id: str
    target_entity_id: str
    relation_type: str
    value: float | bool | str | None


@dataclass(frozen=True, slots=True)
class PublicObservation:
    """Observation returned by the public environment interface."""

    observation_id: str
    step_index: int
    kind: ObservationKind
    entities: Sequence[PublicEntity]
    relations: Sequence[PublicRelation]
    events: Sequence[str]
    timestamp: int


@dataclass(frozen=True, slots=True)
class PublicAction:
    """Action submitted by UNKNOWN."""

    kind: ActionKind
    entity_id: str | None = None
    vector: PublicVector2 | None = None
    parameters: Mapping[str, str | int | float | bool] | None = None


@dataclass(frozen=True, slots=True)
class PublicIntervention:
    """Intervention submitted through the public interface."""

    kind: InterventionKind
    entity_id: str
    vector: PublicVector2 | None = None
    parameters: Mapping[str, str | int | float | bool] | None = None


@dataclass(frozen=True, slots=True)
class PublicStepResult:
    """Public result returned after an action or intervention."""

    observation: PublicObservation
    reward: float
    terminal: bool


@dataclass(frozen=True, slots=True)
class PublicEnvironmentMetadata:
    """Non-semantic metadata exposed by the public environment."""

    experiment_id: str
    environment_version: str
    schema_version: str
    max_steps: int
    action_kinds: Sequence[ActionKind]
    intervention_kinds: Sequence[InterventionKind]


@dataclass(frozen=True, slots=True)
class PublicEnvironmentConfig:
    """Configuration that is safe to expose to UNKNOWN."""

    environment_version: str
    schema_version: str
    max_steps: int
    world_width: float
    world_height: float
    entity_count: int
    observation_history_limit: int
    allowed_action_kinds: Sequence[ActionKind]
    allowed_intervention_kinds: Sequence[InterventionKind]
    public_attributes: Sequence[str]