"""Tests for Project UNKNOWN evaluation schemas."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from unknown.environment.schemas.evaluation import (
    ComplexityRecord,
    DiscoveryEvaluation,
    DiscoveryOutcome,
    EvaluationDimension,
    EvaluationMetric,
    EvaluationOutcome,
    EvaluationRecord,
    FalsificationRecord,
    InterventionRecord,
    RepresentationRecoveryRecord,
    TransferRecord,
)


def test_evaluation_metric_is_immutable() -> None:
    metric = EvaluationMetric(
        name="accuracy",
        value=0.95,
        threshold=0.90,
        unit="ratio",
    )

    with pytest.raises(FrozenInstanceError):
        metric.value = 1.0  # type: ignore[misc]


def test_evaluation_metric_can_represent_thresholded_measurement() -> None:
    metric = EvaluationMetric(
        name="prediction_accuracy",
        value=0.94,
        threshold=0.90,
        unit="ratio",
    )

    assert metric.name == "prediction_accuracy"
    assert metric.value == 0.94
    assert metric.threshold == 0.90
    assert metric.unit == "ratio"


def test_evaluation_record_captures_dimension_and_outcome() -> None:
    metric = EvaluationMetric(
        name="accuracy",
        value=0.95,
        threshold=0.90,
        unit="ratio",
    )

    record = EvaluationRecord(
        evaluation_id="evaluation-001",
        candidate_id="candidate-001",
        dimension=EvaluationDimension.PREDICTION,
        outcome=EvaluationOutcome.PASS,
        metrics=(metric,),
        evidence_reference="evidence/prediction-001.json",
        evaluator_version="0.1.0",
    )

    assert record.evaluation_id == "evaluation-001"
    assert record.candidate_id == "candidate-001"
    assert record.dimension is EvaluationDimension.PREDICTION
    assert record.outcome is EvaluationOutcome.PASS
    assert record.metrics == (metric,)
    assert record.evidence_reference == "evidence/prediction-001.json"
    assert record.evaluator_version == "0.1.0"


def test_falsification_record_captures_expected_and_observed_failure() -> None:
    record = FalsificationRecord(
        falsification_id="falsification-001",
        candidate_id="candidate-001",
        condition="remove_supporting relation",
        expected_failure=True,
        observed_failure=True,
        outcome=EvaluationOutcome.PASS,
        evidence_reference="evidence/falsification-001.json",
    )

    assert record.falsification_id == "falsification-001"
    assert record.candidate_id == "candidate-001"
    assert record.expected_failure is True
    assert record.observed_failure is True
    assert record.outcome is EvaluationOutcome.PASS


def test_transfer_record_captures_unseen_context() -> None:
    metric = EvaluationMetric(
        name="transfer_accuracy",
        value=0.91,
        threshold=0.85,
        unit="ratio",
    )

    record = TransferRecord(
        transfer_id="transfer-001",
        candidate_id="candidate-001",
        source_context="context-A",
        target_context="context-B",
        outcome=EvaluationOutcome.PASS,
        metrics=(metric,),
        evidence_reference="evidence/transfer-001.json",
    )

    assert record.transfer_id == "transfer-001"
    assert record.source_context == "context-A"
    assert record.target_context == "context-B"
    assert record.outcome is EvaluationOutcome.PASS
    assert record.metrics == (metric,)


def test_intervention_record_captures_prediction_and_observation() -> None:
    record = InterventionRecord(
        intervention_id="intervention-001",
        candidate_id="candidate-001",
        intervention_description="increase friction",
        predicted_effect="slower movement",
        observed_effect="slower movement",
        outcome=EvaluationOutcome.PASS,
        evidence_reference="evidence/intervention-001.json",
    )

    assert record.intervention_id == "intervention-001"
    assert record.predicted_effect == "slower movement"
    assert record.observed_effect == "slower movement"
    assert record.outcome is EvaluationOutcome.PASS


def test_representation_recovery_distinguishes_match_types() -> None:
    record = RepresentationRecoveryRecord(
        candidate_id="candidate-001",
        exact_match=False,
        equivalent_match=True,
        predictive_equivalence=True,
        recovered_components=("friction",),
        missing_components=(),
    )

    assert record.exact_match is False
    assert record.equivalent_match is True
    assert record.predictive_equivalence is True
    assert record.recovered_components == ("friction",)
    assert record.missing_components == ()


def test_complexity_record_captures_search_cost() -> None:
    record = ComplexityRecord(
        candidate_id="candidate-001",
        added_components=1,
        expression_complexity=2.5,
        search_cost=14.0,
        description_length=18.0,
    )

    assert record.candidate_id == "candidate-001"
    assert record.added_components == 1
    assert record.expression_complexity == 2.5
    assert record.search_cost == 14.0
    assert record.description_length == 18.0


def test_discovery_evaluation_combines_all_evidence_dimensions() -> None:
    metric = EvaluationMetric(
        name="accuracy",
        value=0.95,
        threshold=0.90,
        unit="ratio",
    )

    evaluation = EvaluationRecord(
        evaluation_id="evaluation-001",
        candidate_id="candidate-001",
        dimension=EvaluationDimension.PREDICTION,
        outcome=EvaluationOutcome.PASS,
        metrics=(metric,),
        evidence_reference=None,
        evaluator_version="0.1.0",
    )

    falsification = FalsificationRecord(
        falsification_id="falsification-001",
        candidate_id="candidate-001",
        condition="counterexample",
        expected_failure=True,
        observed_failure=True,
        outcome=EvaluationOutcome.PASS,
        evidence_reference=None,
    )

    intervention = InterventionRecord(
        intervention_id="intervention-001",
        candidate_id="candidate-001",
        intervention_description="increase friction",
        predicted_effect="slower movement",
        observed_effect="slower movement",
        outcome=EvaluationOutcome.PASS,
        evidence_reference=None,
    )

    transfer = TransferRecord(
        transfer_id="transfer-001",
        candidate_id="candidate-001",
        source_context="A",
        target_context="B",
        outcome=EvaluationOutcome.PASS,
        metrics=(metric,),
        evidence_reference=None,
    )

    recovery = RepresentationRecoveryRecord(
        candidate_id="candidate-001",
        exact_match=False,
        equivalent_match=True,
        predictive_equivalence=True,
        recovered_components=("friction",),
        missing_components=(),
    )

    complexity = ComplexityRecord(
        candidate_id="candidate-001",
        added_components=1,
        expression_complexity=1.0,
        search_cost=2.0,
        description_length=3.0,
    )

    result = DiscoveryEvaluation(
        candidate_id="candidate-001",
        evaluations=(evaluation,),
        falsification=(falsification,),
        interventions=(intervention,),
        transfer=(transfer,),
        representation_recovery=recovery,
        complexity=complexity,
        outcome=DiscoveryOutcome.DISCOVERY_ACCEPTED,
        evaluator_metadata={"evaluator_version": "0.1.0"},
    )

    assert result.candidate_id == "candidate-001"
    assert result.evaluations == (evaluation,)
    assert result.falsification == (falsification,)
    assert result.interventions == (intervention,)
    assert result.transfer == (transfer,)
    assert result.representation_recovery is recovery
    assert result.complexity is complexity
    assert result.outcome is DiscoveryOutcome.DISCOVERY_ACCEPTED


def test_evaluation_dimensions_are_explicit() -> None:
    expected = {
        "prediction",
        "intervention",
        "falsification",
        "transfer",
        "representation_recovery",
        "complexity",
    }

    actual = {dimension.value for dimension in EvaluationDimension}

    assert actual == expected


def test_evaluation_outcomes_are_explicit() -> None:
    expected = {
        "pass",
        "fail",
        "inconclusive",
    }

    actual = {outcome.value for outcome in EvaluationOutcome}

    assert actual == expected


def test_discovery_outcomes_are_explicit() -> None:
    expected = {
        "discovery_accepted",
        "discovery_rejected",
        "representation_failure_correctly_rejected",
        "model_family_failure_correctly_rejected",
        "parameter_failure_correctly_rejected",
        "information_unavailable_correctly_rejected",
        "inconclusive",
    }

    actual = {outcome.value for outcome in DiscoveryOutcome}

    assert actual == expected