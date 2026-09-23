"""Boundary contract tests for Project UNKNOWN.

These tests define the scientific separation between:

- public information available to UNKNOWN
- hidden benchmark truth
- evaluation-only information

The runtime implementation will be required to satisfy these contracts.
"""

from __future__ import annotations

from dataclasses import fields

from unknown.environment.schemas.evaluation import (
    DiscoveryEvaluation,
    EvaluationRecord,
)
from unknown.environment.schemas.hidden import (
    GroundTruthRepresentation,
    HiddenCondition,
    HiddenEnvironmentState,
    HiddenState,
)
from unknown.environment.schemas.public import (
    PublicAction,
    PublicEnvironmentConfig,
    PublicEnvironmentMetadata,
    PublicObservation,
    PublicStepResult,
)


def _field_names(schema_type: type[object]) -> set[str]:
    """Return dataclass field names for a schema type."""
    return {field.name for field in fields(schema_type)}


def test_public_observation_has_no_hidden_truth_fields() -> None:
    public_fields = _field_names(PublicObservation)

    forbidden_fields = {
        "hidden_state",
        "ground_truth",
        "ground_truth_representation",
        "condition",
        "benchmark_condition",
        "evaluation_label",
        "evaluation_score",
        "oracle",
    }

    assert public_fields.isdisjoint(forbidden_fields)


def test_public_step_result_has_no_hidden_truth_fields() -> None:
    public_fields = _field_names(PublicStepResult)

    forbidden_fields = {
        "hidden_state",
        "ground_truth",
        "ground_truth_representation",
        "condition",
        "benchmark_condition",
        "evaluation_label",
        "evaluation_score",
        "oracle",
    }

    assert public_fields.isdisjoint(forbidden_fields)


def test_public_action_has_no_hidden_truth_fields() -> None:
    public_fields = _field_names(PublicAction)

    forbidden_fields = {
        "hidden_state",
        "ground_truth",
        "ground_truth_representation",
        "condition",
        "benchmark_condition",
        "evaluation_label",
        "evaluation_score",
        "oracle",
    }

    assert public_fields.isdisjoint(forbidden_fields)


def test_public_environment_config_has_no_hidden_truth_fields() -> None:
    public_fields = _field_names(PublicEnvironmentConfig)

    forbidden_fields = {
        "hidden_state",
        "ground_truth",
        "ground_truth_representation",
        "condition",
        "benchmark_condition",
        "evaluation_label",
        "evaluation_score",
        "oracle",
    }

    assert public_fields.isdisjoint(forbidden_fields)


def test_public_environment_metadata_has_no_hidden_truth_fields() -> None:
    public_fields = _field_names(PublicEnvironmentMetadata)

    forbidden_fields = {
        "hidden_state",
        "ground_truth",
        "ground_truth_representation",
        "condition",
        "benchmark_condition",
        "evaluation_label",
        "evaluation_score",
        "oracle",
    }

    assert public_fields.isdisjoint(forbidden_fields)


def test_hidden_environment_state_contains_private_truth_fields() -> None:
    hidden_fields = _field_names(HiddenEnvironmentState)

    required_hidden_fields = {
        "hidden_state",
        "ground_truth_representation",
        "condition",
        "private_metadata",
    }

    assert required_hidden_fields.issubset(hidden_fields)


def test_hidden_state_is_separate_from_public_observation() -> None:
    hidden_fields = _field_names(HiddenState)
    public_fields = _field_names(PublicObservation)

    assert hidden_fields != public_fields


def test_ground_truth_representation_is_not_a_public_schema() -> None:
    hidden_fields = _field_names(GroundTruthRepresentation)
    public_fields = _field_names(PublicObservation)

    assert hidden_fields != public_fields


def test_hidden_condition_is_not_a_public_schema() -> None:
    hidden_fields = _field_names(HiddenCondition)
    public_fields = _field_names(PublicObservation)

    assert hidden_fields != public_fields


def test_evaluation_record_is_separate_from_public_observation() -> None:
    evaluation_fields = _field_names(EvaluationRecord)
    public_fields = _field_names(PublicObservation)

    assert evaluation_fields != public_fields


def test_discovery_evaluation_is_separate_from_public_observation() -> None:
    evaluation_fields = _field_names(DiscoveryEvaluation)
    public_fields = _field_names(PublicObservation)

    assert evaluation_fields != public_fields


def test_public_and_hidden_schema_modules_are_distinct() -> None:
    assert PublicObservation.__module__.startswith(
        "unknown.environment.schemas.public"
    )
    assert HiddenState.__module__.startswith(
        "unknown.environment.schemas.hidden"
    )


def test_public_and_evaluation_schema_modules_are_distinct() -> None:
    assert PublicObservation.__module__.startswith(
        "unknown.environment.schemas.public"
    )
    assert EvaluationRecord.__module__.startswith(
        "unknown.environment.schemas.evaluation"
    )


def test_public_and_hidden_objects_are_not_interchangeable() -> None:
    public_observation = PublicObservation(
        observation_id="observation-001",
        step_index=0,
        kind="state",
        entities=(),
        relations=(),
        events=(),
        timestamp=0,
    )

    hidden_state = HiddenState(
        step_index=0,
        variables=(),
        relations=(),
    )

    assert not isinstance(public_observation, HiddenState)
    assert not isinstance(hidden_state, PublicObservation)