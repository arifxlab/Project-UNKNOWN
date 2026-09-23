"""Executable leakage-boundary tests for Project UNKNOWN.

These tests enforce the S0.4 scientific boundary between:

- information legitimately available to UNKNOWN
- hidden benchmark truth
- evaluation-only information

The purpose is not to prove that the entire future benchmark is leakage-free.
The purpose is to make the currently implemented public boundary fail loudly
if hidden or evaluation concepts are introduced accidentally.
"""

from __future__ import annotations

import inspect
from dataclasses import fields
from typing import get_type_hints

import unknown.environment.public.runtime as public_runtime_module
from unknown.environment.public.runtime import PublicEnvironmentRuntime
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
    PublicIntervention,
    PublicObservation,
    PublicStepResult,
)


FORBIDDEN_NAMES = {
    "hidden_state",
    "ground_truth",
    "ground_truth_representation",
    "condition",
    "benchmark_condition",
    "evaluation",
    "evaluation_record",
    "discovery_evaluation",
    "evaluation_label",
    "evaluation_score",
    "oracle",
}


def _field_names(schema_type: type[object]) -> set[str]:
    """Return dataclass field names for a schema."""
    return {field.name for field in fields(schema_type)}


def _minimal_config() -> PublicEnvironmentConfig:
    """Build a minimal valid public configuration."""
    return PublicEnvironmentConfig(
        environment_version="0.1.0",
        schema_version="0.1.0",
        max_steps=3,
        world_width=100.0,
        world_height=100.0,
        entity_count=0,
        observation_history_limit=10,
        allowed_action_kinds=(),
        allowed_intervention_kinds=(),
        public_attributes=(),
    )


def test_public_observation_has_no_forbidden_truth_fields() -> None:
    """Public observations must not expose benchmark truth."""
    assert _field_names(PublicObservation).isdisjoint(FORBIDDEN_NAMES)


def test_public_action_has_no_forbidden_truth_fields() -> None:
    """Public actions must not contain benchmark truth."""
    assert _field_names(PublicAction).isdisjoint(FORBIDDEN_NAMES)


def test_public_intervention_has_no_forbidden_truth_fields() -> None:
    """Public interventions must not contain benchmark truth."""
    assert _field_names(PublicIntervention).isdisjoint(FORBIDDEN_NAMES)


def test_public_step_result_has_no_forbidden_truth_fields() -> None:
    """Public step results must not contain benchmark truth."""
    assert _field_names(PublicStepResult).isdisjoint(FORBIDDEN_NAMES)


def test_public_environment_config_has_no_forbidden_truth_fields() -> None:
    """Public configuration must not contain benchmark labels or oracles."""
    assert _field_names(PublicEnvironmentConfig).isdisjoint(FORBIDDEN_NAMES)


def test_public_environment_metadata_has_no_forbidden_truth_fields() -> None:
    """Public metadata must not contain benchmark labels or scores."""
    assert _field_names(PublicEnvironmentMetadata).isdisjoint(FORBIDDEN_NAMES)


def test_hidden_schema_contains_truth_fields_separately() -> None:
    """Hidden benchmark truth must remain represented by hidden schemas."""
    assert {
        "hidden_state",
        "ground_truth_representation",
        "condition",
    }.issubset(_field_names(HiddenEnvironmentState))


def test_evaluation_schema_remains_separate() -> None:
    """Evaluation objects must remain distinct from public observations."""
    assert _field_names(EvaluationRecord) != _field_names(PublicObservation)
    assert _field_names(DiscoveryEvaluation) != _field_names(
        PublicObservation
    )


def test_public_runtime_instance_has_no_forbidden_attributes() -> None:
    """Runtime instances must not store hidden or evaluation state."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=_minimal_config(), seed=1)

    assert set(vars(runtime)).isdisjoint(FORBIDDEN_NAMES)


def test_public_runtime_module_does_not_import_hidden_schema_module() -> None:
    """Public runtime must not directly import hidden benchmark schemas."""
    source = inspect.getsource(public_runtime_module)

    forbidden_imports = {
        "unknown.environment.schemas.hidden",
        "unknown.environment.schemas.evaluation",
    }

    assert all(path not in source for path in forbidden_imports)


def test_public_runtime_module_does_not_reference_hidden_truth_names() -> None:
    """Public runtime source must not reference benchmark truth concepts."""
    source = inspect.getsource(public_runtime_module)

    forbidden_source_tokens = {
        "GroundTruthRepresentation",
        "HiddenEnvironmentState",
        "HiddenState",
        "HiddenCondition",
        "DiscoveryEvaluation",
        "EvaluationRecord",
    }

    assert all(token not in source for token in forbidden_source_tokens)


def test_public_runtime_annotations_remain_public() -> None:
    """Runtime method annotations must use public-facing schemas only."""
    public_runtime = PublicEnvironmentRuntime

    reset_hints = get_type_hints(public_runtime.reset)
    observe_hints = get_type_hints(public_runtime.observe)
    step_hints = get_type_hints(public_runtime.step)
    intervene_hints = get_type_hints(public_runtime.intervene)
    metadata_hints = get_type_hints(public_runtime.episode_metadata)

    forbidden_types = {
        HiddenState,
        HiddenEnvironmentState,
        HiddenCondition,
        GroundTruthRepresentation,
        EvaluationRecord,
        DiscoveryEvaluation,
    }

    for hints in (
        reset_hints,
        observe_hints,
        step_hints,
        intervene_hints,
        metadata_hints,
    ):
        assert forbidden_types.isdisjoint(set(hints.values()))


def test_public_observation_module_is_public() -> None:
    """Public observation schema must belong to the public module."""
    assert PublicObservation.__module__ == (
        "unknown.environment.schemas.public"
    )


def test_hidden_objects_are_not_public_objects() -> None:
    """Hidden benchmark objects must not be instances of public schemas."""
    assert not isinstance(HiddenState(0, (), ()), PublicObservation)

    hidden_condition = HiddenCondition(
        condition_id="condition-001",
        kind="representation_failure",
        description="synthetic hidden condition",
        required_information=(),
        available_through_observation=True,
        expressible_by_extension_language=True,
        ground_truth_representation_id="representation-001",
    )

    assert not isinstance(hidden_condition, PublicObservation)


def test_ground_truth_is_not_public_metadata() -> None:
    """Ground-truth representation must remain outside public metadata."""
    ground_truth = GroundTruthRepresentation(
        representation_id="representation-001",
        variables=("position",),
        relations=(),
        sufficient_for_target=True,
    )

    metadata_fields = _field_names(PublicEnvironmentMetadata)

    assert "representation_id" not in metadata_fields
    assert "variables" not in metadata_fields
    assert "sufficient_for_target" not in metadata_fields
    assert ground_truth.representation_id != getattr(
        PublicEnvironmentMetadata,
        "representation_id",
        None,
    )


def test_hidden_environment_state_is_not_public_runtime_state() -> None:
    """Hidden environment state must not be exposed by the runtime object."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=_minimal_config(), seed=1)

    hidden_state = HiddenEnvironmentState(
        hidden_state=HiddenState(
            step_index=0,
            variables=(),
            relations=(),
        ),
        ground_truth_representation=GroundTruthRepresentation(
            representation_id="representation-001",
            variables=(),
            relations=(),
            sufficient_for_target=False,
        ),
        condition=HiddenCondition(
            condition_id="condition-001",
            kind="information_unavailable",
            description="hidden benchmark condition",
            required_information=(),
            available_through_observation=False,
            expressible_by_extension_language=False,
            ground_truth_representation_id="representation-001",
        ),
        private_metadata={},
    )

    assert "hidden_state" not in vars(runtime)
    assert "ground_truth_representation" not in vars(runtime)
    assert "condition" not in vars(runtime)
    assert hidden_state not in vars(runtime).values()


def test_public_runtime_returns_public_observation_type() -> None:
    """Runtime observation output must be the public observation schema."""
    runtime = PublicEnvironmentRuntime()
    observation = runtime.reset(config=_minimal_config(), seed=1)

    assert isinstance(observation, PublicObservation)


def test_public_runtime_metadata_returns_public_type() -> None:
    """Runtime metadata output must be the public metadata schema."""
    runtime = PublicEnvironmentRuntime()
    runtime.reset(config=_minimal_config(), seed=1)

    metadata = runtime.episode_metadata()

    assert isinstance(metadata, PublicEnvironmentMetadata)


def test_public_runtime_has_no_evaluation_output_surface() -> None:
    """Runtime must not expose an evaluation result accessor."""
    runtime = PublicEnvironmentRuntime()

    forbidden_methods = {
        "evaluate",
        "evaluation",
        "get_evaluation",
        "get_ground_truth",
        "get_hidden_state",
        "oracle",
    }

    public_attributes = set(dir(runtime))

    assert forbidden_methods.isdisjoint(public_attributes)