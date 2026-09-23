"""Public observation projection for Project UNKNOWN.

The observation projector implements the public information boundary:

    P : S_t -> O_t

Only information explicitly permitted by the public observation contract may
cross this boundary.

Scientific boundary
-------------------
This module must not:

- import hidden-state schemas
- import evaluation schemas
- inspect benchmark conditions
- inspect ground-truth representations
- inspect evaluator state
- derive hidden semantic labels
- expose internal-only physical properties
- access external services
- mutate the source WorldState

The projector is deterministic and side-effect free.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Final

from unknown.environment.dynamics.models import (
    EntityState,
    RelationState,
    WorldState,
)
from unknown.environment.schemas.public import (
    ObservationKind,
    PublicEntity,
    PublicObservation,
    PublicRelation,
    PublicVector2,
)


class ObservationProjectionError(ValueError):
    """Raised when public observation projection cannot be completed safely."""


class PublicObservationProjector:
    """Project internal world state into a public observation.

    The projector deliberately exposes only the primitive quantities defined
    by the S0.5-C observation contract.

    Public entity fields:
        - opaque entity identifier
        - position
        - velocity
        - explicitly permitted public attributes

    Public relation fields:
        - relation identifier
        - source entity identifier
        - target entity identifier
        - explicitly permitted relation type
        - public relation value when supplied

    Internal-only fields such as mass and semantic entity category are never
    copied into the public representation.
    """

    _OBSERVATION_ID_PREFIX: Final[str] = "observation"

    def project(
        self,
        world_state: WorldState,
        *,
        events: Sequence[str] = (),
    ) -> PublicObservation:
        """Project a WorldState into a PublicObservation.

        Args:
            world_state: Internal deterministic world state.
            events: Explicitly public events generated for this observation.

        Returns:
            A deterministic public observation.

        Raises:
            ObservationProjectionError:
                If the world state contains invalid public-boundary data.
        """
        self._validate_world_state(world_state)
        self._validate_events(events)

        entities = tuple(
            self._project_entity(entity)
            for entity in world_state.entities
        )

        relations = tuple(
            self._project_relation(relation)
            for relation in world_state.relations
        )

        return PublicObservation(
            observation_id=self._observation_id(world_state.step_index),
            step_index=world_state.step_index,
            kind=ObservationKind.STATE,
            entities=entities,
            relations=relations,
            events=tuple(events),
            timestamp=self._timestamp(world_state),
        )

    @classmethod
    def _project_entity(cls, entity: EntityState) -> PublicEntity:
        """Project only contract-approved entity information.

        Mass and semantic category are intentionally ignored.
        """

        return PublicEntity(
            entity_id=entity.entity_id,
            position=PublicVector2(
                x=entity.position.x,
                y=entity.position.y,
            ),
            velocity=PublicVector2(
                x=entity.velocity.x,
                y=entity.velocity.y,
            ),
            attributes={},
        )

    @staticmethod
    def _project_relation(relation: RelationState) -> PublicRelation:
        """Project an explicitly public relation.

        RelationState currently contains only relation information that has
        already been defined as publicly observable by the dynamics contract.
        No hidden relation metadata is consulted or inferred.
        """

        return PublicRelation(
            relation_id=relation.relation_id,
            source_entity_id=relation.source_entity_id,
            target_entity_id=relation.target_entity_id,
            relation_type=relation.relation_type,
            value=None,
        )

    @classmethod
    def _observation_id(cls, step_index: int) -> str:
        """Create a deterministic observation identifier."""

        return f"{cls._OBSERVATION_ID_PREFIX}-{step_index:08d}"

    @staticmethod
    def _timestamp(world_state: WorldState) -> int:
        """Return deterministic simulation time.

        The current public schema represents timestamps as integer simulation
        ticks. Wall-clock time is deliberately excluded.
        """

        return world_state.step_index

    @staticmethod
    def _validate_world_state(world_state: WorldState) -> None:
        """Validate only invariants required by the public boundary."""

        if not isinstance(world_state, WorldState):
            raise ObservationProjectionError(
                "world_state must be a WorldState instance."
            )

        if world_state.step_index < 0:
            raise ObservationProjectionError(
                "world_state step_index must be non-negative."
            )

        entity_ids: set[str] = set()

        for entity in world_state.entities:
            if not isinstance(entity, EntityState):
                raise ObservationProjectionError(
                    "world_state contains an invalid entity."
                )

            if not entity.entity_id:
                raise ObservationProjectionError(
                    "world_state contains an entity without an identifier."
                )

            if entity.entity_id in entity_ids:
                raise ObservationProjectionError(
                    "world_state contains duplicate entity identifiers."
                )

            entity_ids.add(entity.entity_id)

        relation_ids: set[str] = set()

        for relation in world_state.relations:
            if not isinstance(relation, RelationState):
                raise ObservationProjectionError(
                    "world_state contains an invalid relation."
                )

            if not relation.relation_id:
                raise ObservationProjectionError(
                    "world_state contains a relation without an identifier."
                )

            if relation.relation_id in relation_ids:
                raise ObservationProjectionError(
                    "world_state contains duplicate relation identifiers."
                )

            if relation.source_entity_id not in entity_ids:
                raise ObservationProjectionError(
                    "world_state contains a relation with an unknown source."
                )

            if relation.target_entity_id not in entity_ids:
                raise ObservationProjectionError(
                    "world_state contains a relation with an unknown target."
                )

            relation_ids.add(relation.relation_id)

    @staticmethod
    def _validate_events(events: Sequence[str]) -> None:
        """Validate the explicitly public event channel."""

        if isinstance(events, (str, bytes)):
            raise ObservationProjectionError(
                "events must be a sequence of event strings."
            )

        for event in events:
            if not isinstance(event, str):
                raise ObservationProjectionError(
                    "public observation events must be strings."
                )