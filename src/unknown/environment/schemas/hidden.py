"""Hidden benchmark schemas for Project UNKNOWN.

These schemas contain benchmark truth that is intentionally unavailable to
the UNKNOWN discovery system during normal environment interaction.

Scientific boundary
-------------------
Objects in this module are benchmark-side objects.

They may contain:

- latent state
- ground-truth representations
- causal structure
- benchmark condition labels
- hidden relations
- information-availability labels
- representation-failure labels
- model-family-failure labels
- parameter-failure labels

They must never be returned through the public environment interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class HiddenConditionKind(str, Enum):
    """Ground-truth benchmark condition."""

    INFORMATION_UNAVAILABLE = "information_unavailable"
    REPRESENTATION_FAILURE = "representation_failure"
    MODEL_FAMILY_FAILURE = "model_family_failure"
    PARAMETER_FAILURE = "parameter_failure"
    LANGUAGE_INSUFFICIENCY = "language_insufficiency"


class HiddenVariableKind(str, Enum):
    """Kinds of latent variables used by the benchmark."""

    POSITION = "position"
    VELOCITY = "velocity"
    MASS = "mass"
    FRICTION = "friction"
    RELATION = "relation"
    CATEGORY = "category"
    CONTEXT = "context"


@dataclass(frozen=True, slots=True)
class HiddenVector2:
    """Two-dimensional hidden vector."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class HiddenVariable:
    """A benchmark-side latent variable."""

    variable_id: str
    kind: HiddenVariableKind
    value: str | int | float | bool | HiddenVector2


@dataclass(frozen=True, slots=True)
class HiddenRelation:
    """A benchmark-side relation unavailable to UNKNOWN."""

    relation_id: str
    source_entity_id: str
    target_entity_id: str
    relation_type: str
    value: str | int | float | bool | None


@dataclass(frozen=True, slots=True)
class HiddenState:
    """Complete benchmark-side latent state."""

    step_index: int
    variables: Sequence[HiddenVariable]
    relations: Sequence[HiddenRelation]


@dataclass(frozen=True, slots=True)
class GroundTruthRepresentation:
    """Ground-truth representation known only to the benchmark."""

    representation_id: str
    variables: Sequence[str]
    relations: Sequence[str]
    sufficient_for_target: bool


@dataclass(frozen=True, slots=True)
class HiddenCondition:
    """Ground-truth explanation for a benchmark condition."""

    condition_id: str
    kind: HiddenConditionKind
    description: str
    required_information: Sequence[str]
    available_through_observation: bool
    expressible_by_extension_language: bool
    ground_truth_representation_id: str


@dataclass(frozen=True, slots=True)
class HiddenEnvironmentState:
    """Benchmark-side environment state.

    This object must never cross the public API boundary.
    """

    hidden_state: HiddenState
    ground_truth_representation: GroundTruthRepresentation
    condition: HiddenCondition
    private_metadata: Mapping[str, str | int | float | bool]


@dataclass(frozen=True, slots=True)
class HiddenEpisodeRecord:
    """Complete hidden record for one benchmark episode."""

    episode_id: str
    environment_state: HiddenEnvironmentState
    state_history: Sequence[HiddenState]
    condition_history: Sequence[HiddenCondition]