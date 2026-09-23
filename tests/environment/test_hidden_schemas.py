"""Tests for Project UNKNOWN hidden benchmark schemas."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from unknown.environment.schemas.hidden import (
    GroundTruthRepresentation,
    HiddenCondition,
    HiddenConditionKind,
    HiddenEnvironmentState,
    HiddenEpisodeRecord,
    HiddenRelation,
    HiddenState,
    HiddenVariable,
    HiddenVariableKind,
    HiddenVector2,
)


def test_hidden_vector_is_immutable() -> None:
    vector = HiddenVector2(x=1.0, y=2.0)

    with pytest.raises(FrozenInstanceError):
        vector.x = 5.0  # type: ignore[misc]


def test_hidden_variable_can_represent_latent_value() -> None:
    variable = HiddenVariable(
        variable_id="latent-001",
        kind=HiddenVariableKind.FRICTION,
        value=0.75,
    )

    assert variable.variable_id == "latent-001"
    assert variable.kind is HiddenVariableKind.FRICTION
    assert variable.value == 0.75


def test_hidden_relation_can_store_benchmark_truth() -> None:
    relation = HiddenRelation(
        relation_id="hidden-relation-001",
        source_entity_id="entity-001",
        target_entity_id="entity-002",
        relation_type="causes",
        value=True,
    )

    assert relation.relation_id == "hidden-relation-001"
    assert relation.source_entity_id == "entity-001"
    assert relation.target_entity_id == "entity-002"
    assert relation.relation_type == "causes"
    assert relation.value is True


def test_hidden_state_contains_latent_variables_and_relations() -> None:
    variable = HiddenVariable(
        variable_id="latent-001",
        kind=HiddenVariableKind.MASS,
        value=10.0,
    )

    relation = HiddenRelation(
        relation_id="hidden-relation-001",
        source_entity_id="entity-001",
        target_entity_id="entity-002",
        relation_type="causes",
        value=True,
    )

    state = HiddenState(
        step_index=3,
        variables=(variable,),
        relations=(relation,),
    )

    assert state.step_index == 3
    assert state.variables == (variable,)
    assert state.relations == (relation,)


def test_ground_truth_representation_records_benchmark_truth() -> None:
    representation = GroundTruthRepresentation(
        representation_id="ground-truth-001",
        variables=("mass", "friction"),
        relations=("causal_influence",),
        sufficient_for_target=True,
    )

    assert representation.representation_id == "ground-truth-001"
    assert representation.variables == ("mass", "friction")
    assert representation.relations == ("causal_influence",)
    assert representation.sufficient_for_target is True


def test_hidden_condition_distinguishes_representation_failure() -> None:
    condition = HiddenCondition(
        condition_id="condition-001",
        kind=HiddenConditionKind.REPRESENTATION_FAILURE,
        description="Required distinction is observable but absent from the current representation.",
        required_information=("friction",),
        available_through_observation=True,
        expressible_by_extension_language=True,
        ground_truth_representation_id="ground-truth-001",
    )

    assert condition.kind is HiddenConditionKind.REPRESENTATION_FAILURE
    assert condition.available_through_observation is True
    assert condition.expressible_by_extension_language is True


def test_hidden_condition_distinguishes_information_unavailable() -> None:
    condition = HiddenCondition(
        condition_id="condition-002",
        kind=HiddenConditionKind.INFORMATION_UNAVAILABLE,
        description="Required distinction is absent from the permitted observation interface.",
        required_information=("hidden_context",),
        available_through_observation=False,
        expressible_by_extension_language=True,
        ground_truth_representation_id="ground-truth-002",
    )

    assert condition.kind is HiddenConditionKind.INFORMATION_UNAVAILABLE
    assert condition.available_through_observation is False
    assert condition.expressible_by_extension_language is True


def test_hidden_environment_state_contains_private_truth() -> None:
    hidden_state = HiddenState(
        step_index=0,
        variables=(),
        relations=(),
    )

    representation = GroundTruthRepresentation(
        representation_id="ground-truth-001",
        variables=("mass",),
        relations=(),
        sufficient_for_target=True,
    )

    condition = HiddenCondition(
        condition_id="condition-001",
        kind=HiddenConditionKind.REPRESENTATION_FAILURE,
        description="Benchmark condition.",
        required_information=("mass",),
        available_through_observation=True,
        expressible_by_extension_language=True,
        ground_truth_representation_id="ground-truth-001",
    )

    environment_state = HiddenEnvironmentState(
        hidden_state=hidden_state,
        ground_truth_representation=representation,
        condition=condition,
        private_metadata={"benchmark_seed": 12345},
    )

    assert environment_state.hidden_state is hidden_state
    assert environment_state.ground_truth_representation is representation
    assert environment_state.condition is condition
    assert environment_state.private_metadata["benchmark_seed"] == 12345


def test_hidden_episode_record_contains_private_history() -> None:
    hidden_state = HiddenState(
        step_index=0,
        variables=(),
        relations=(),
    )

    representation = GroundTruthRepresentation(
        representation_id="ground-truth-001",
        variables=(),
        relations=(),
        sufficient_for_target=True,
    )

    condition = HiddenCondition(
        condition_id="condition-001",
        kind=HiddenConditionKind.PARAMETER_FAILURE,
        description="Parameter configuration prevents the current model from fitting.",
        required_information=(),
        available_through_observation=True,
        expressible_by_extension_language=True,
        ground_truth_representation_id="ground-truth-001",
    )

    environment_state = HiddenEnvironmentState(
        hidden_state=hidden_state,
        ground_truth_representation=representation,
        condition=condition,
        private_metadata={"benchmark_seed": 12345},
    )

    record = HiddenEpisodeRecord(
        episode_id="episode-001",
        environment_state=environment_state,
        state_history=(hidden_state,),
        condition_history=(condition,),
    )

    assert record.episode_id == "episode-001"
    assert record.environment_state is environment_state
    assert record.state_history == (hidden_state,)
    assert record.condition_history == (condition,)


def test_hidden_condition_kinds_are_explicit() -> None:
    expected = {
        "information_unavailable",
        "representation_failure",
        "model_family_failure",
        "parameter_failure",
        "language_insufficiency",
    }

    actual = {condition.value for condition in HiddenConditionKind}

    assert actual == expected


def test_hidden_variable_kinds_are_explicit() -> None:
    expected = {
        "position",
        "velocity",
        "mass",
        "friction",
        "relation",
        "category",
        "context",
    }

    actual = {variable.value for variable in HiddenVariableKind}

    assert actual == expected