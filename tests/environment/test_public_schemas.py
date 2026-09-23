"""Tests for Project UNKNOWN public environment schemas."""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace

import pytest

from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    ObservationKind,
    PublicAction,
    PublicEntity,
    PublicEnvironmentConfig,
    PublicEnvironmentMetadata,
    PublicIntervention,
    PublicObservation,
    PublicRelation,
    PublicStepResult,
    PublicVector2,
)


def test_public_vector_is_immutable() -> None:
    vector = PublicVector2(x=1.0, y=2.0)

    with pytest.raises(FrozenInstanceError):
        vector.x = 5.0  # type: ignore[misc]


def test_public_entity_preserves_opaque_identifier() -> None:
    entity = PublicEntity(
        entity_id="entity-001",
        position=PublicVector2(x=1.0, y=2.0),
        velocity=PublicVector2(x=0.5, y=-0.25),
        attributes={"size": 1.0, "active": True},
    )

    assert entity.entity_id == "entity-001"
    assert entity.position.x == 1.0
    assert entity.position.y == 2.0
    assert entity.velocity.x == 0.5
    assert entity.velocity.y == -0.25
    assert entity.attributes["active"] is True


def test_public_relation_contains_only_public_relation_data() -> None:
    relation = PublicRelation(
        relation_id="relation-001",
        source_entity_id="entity-001",
        target_entity_id="entity-002",
        relation_type="near",
        value=True,
    )

    assert relation.relation_id == "relation-001"
    assert relation.source_entity_id == "entity-001"
    assert relation.target_entity_id == "entity-002"
    assert relation.relation_type == "near"
    assert relation.value is True


def test_public_observation_can_be_constructed() -> None:
    observation = PublicObservation(
        observation_id="observation-001",
        step_index=0,
        kind=ObservationKind.STATE,
        entities=(),
        relations=(),
        events=(),
        timestamp=0,
    )

    assert observation.observation_id == "observation-001"
    assert observation.step_index == 0
    assert observation.kind is ObservationKind.STATE
    assert observation.entities == ()
    assert observation.relations == ()
    assert observation.events == ()
    assert observation.timestamp == 0


def test_public_action_supports_no_op() -> None:
    action = PublicAction(kind=ActionKind.NO_OP)

    assert action.kind is ActionKind.NO_OP
    assert action.entity_id is None
    assert action.vector is None
    assert action.parameters is None


def test_public_action_supports_entity_vector() -> None:
    action = PublicAction(
        kind=ActionKind.MOVE,
        entity_id="entity-001",
        vector=PublicVector2(x=1.0, y=0.0),
        parameters={"duration": 1},
    )

    assert action.kind is ActionKind.MOVE
    assert action.entity_id == "entity-001"
    assert action.vector == PublicVector2(x=1.0, y=0.0)
    assert action.parameters == {"duration": 1}


def test_public_intervention_can_be_constructed() -> None:
    intervention = PublicIntervention(
        kind=InterventionKind.SET_POSITION,
        entity_id="entity-001",
        vector=PublicVector2(x=5.0, y=6.0),
    )

    assert intervention.kind is InterventionKind.SET_POSITION
    assert intervention.entity_id == "entity-001"
    assert intervention.vector == PublicVector2(x=5.0, y=6.0)


def test_public_step_result_contains_no_hidden_evaluation_fields() -> None:
    observation = PublicObservation(
        observation_id="observation-001",
        step_index=1,
        kind=ObservationKind.STATE,
        entities=(),
        relations=(),
        events=(),
        timestamp=1,
    )

    result = PublicStepResult(
        observation=observation,
        reward=0.0,
        terminal=False,
    )

    assert result.observation is observation
    assert result.reward == 0.0
    assert result.terminal is False

    public_fields = set(result.__dataclass_fields__)
    forbidden_names = {
        "hidden_state",
        "ground_truth",
        "benchmark_condition",
        "evaluation_label",
        "oracle",
        "evaluation_score",
    }

    assert public_fields.isdisjoint(forbidden_names)


def test_public_environment_metadata_contains_only_operational_metadata() -> None:
    metadata = PublicEnvironmentMetadata(
        experiment_id="opaque-experiment-001",
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=100,
        action_kinds=(ActionKind.NO_OP, ActionKind.MOVE),
        intervention_kinds=(InterventionKind.SET_POSITION,),
    )

    assert metadata.experiment_id == "opaque-experiment-001"
    assert metadata.environment_version == "0.1.0"
    assert metadata.schema_version == "0.1.0"
    assert metadata.max_steps == 100
    assert metadata.action_kinds == (ActionKind.NO_OP, ActionKind.MOVE)
    assert metadata.intervention_kinds == (InterventionKind.SET_POSITION,)


def test_public_environment_config_is_constructible() -> None:
    config = PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=100,
        world_width=100.0,
        world_height=100.0,
        entity_count=5,
        observation_history_limit=10,
        allowed_action_kinds=(ActionKind.NO_OP, ActionKind.MOVE),
        allowed_intervention_kinds=(InterventionKind.SET_POSITION,),
        public_attributes=("size", "active"),
    )

    assert config.environment_version == "0.1.0"
    assert config.schema_version == "0.1.0"
    assert config.max_steps == 100
    assert config.world_width == 100.0
    assert config.world_height == 100.0
    assert config.entity_count == 5
    assert config.observation_history_limit == 10
    assert config.allowed_action_kinds == (ActionKind.NO_OP, ActionKind.MOVE)
    assert config.allowed_intervention_kinds == (
        InterventionKind.SET_POSITION,
    )
    assert config.public_attributes == ("size", "active")


def test_dataclass_replace_creates_new_public_value() -> None:
    original = PublicVector2(x=1.0, y=2.0)
    updated = replace(original, x=10.0)

    assert original.x == 1.0
    assert original.y == 2.0
    assert updated.x == 10.0
    assert updated.y == 2.0
    assert original != updated