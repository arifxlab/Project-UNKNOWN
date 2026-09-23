"""Evaluation schemas for Project UNKNOWN.

These schemas contain benchmark-side evaluation records.

Scientific boundary
-------------------
Evaluation objects are produced after or independently of the discovery
process. They may reference hidden benchmark truth and measured outcomes,
but they must not be exposed to UNKNOWN as discovery-time information.

The evaluator is therefore a separate scientific boundary from both:

- the public environment interface
- the hidden benchmark state
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence


class EvaluationDimension(str, Enum):
    """Dimensions used to evaluate a discovered representation."""

    PREDICTION = "prediction"
    INTERVENTION = "intervention"
    FALSIFICATION = "falsification"
    TRANSFER = "transfer"
    REPRESENTATION_RECOVERY = "representation_recovery"
    COMPLEXITY = "complexity"


class EvaluationOutcome(str, Enum):
    """Outcome of an individual evaluation."""

    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"


class DiscoveryOutcome(str, Enum):
    """Overall benchmark classification."""

    DISCOVERY_ACCEPTED = "discovery_accepted"
    DISCOVERY_REJECTED = "discovery_rejected"
    REPRESENTATION_FAILURE_CORRECTLY_REJECTED = (
        "representation_failure_correctly_rejected"
    )
    MODEL_FAMILY_FAILURE_CORRECTLY_REJECTED = (
        "model_family_failure_correctly_rejected"
    )
    PARAMETER_FAILURE_CORRECTLY_REJECTED = "parameter_failure_correctly_rejected"
    INFORMATION_UNAVAILABLE_CORRECTLY_REJECTED = (
        "information_unavailable_correctly_rejected"
    )
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class EvaluationMetric:
    """One quantitative evaluation measurement."""

    name: str
    value: float
    threshold: float | None
    unit: str | None


@dataclass(frozen=True, slots=True)
class EvaluationRecord:
    """Evaluation result for one candidate and one dimension."""

    evaluation_id: str
    candidate_id: str
    dimension: EvaluationDimension
    outcome: EvaluationOutcome
    metrics: Sequence[EvaluationMetric]
    evidence_reference: str | None
    evaluator_version: str


@dataclass(frozen=True, slots=True)
class FalsificationRecord:
    """Record describing an attempt to falsify a candidate."""

    falsification_id: str
    candidate_id: str
    condition: str
    expected_failure: bool
    observed_failure: bool
    outcome: EvaluationOutcome
    evidence_reference: str | None


@dataclass(frozen=True, slots=True)
class TransferRecord:
    """Record of candidate performance in an unseen context."""

    transfer_id: str
    candidate_id: str
    source_context: str
    target_context: str
    outcome: EvaluationOutcome
    metrics: Sequence[EvaluationMetric]
    evidence_reference: str | None


@dataclass(frozen=True, slots=True)
class InterventionRecord:
    """Record of candidate behavior under intervention."""

    intervention_id: str
    candidate_id: str
    intervention_description: str
    predicted_effect: str
    observed_effect: str
    outcome: EvaluationOutcome
    evidence_reference: str | None


@dataclass(frozen=True, slots=True)
class RepresentationRecoveryRecord:
    """Record of comparison against benchmark representation truth."""

    candidate_id: str
    exact_match: bool
    equivalent_match: bool
    predictive_equivalence: bool
    recovered_components: Sequence[str]
    missing_components: Sequence[str]


@dataclass(frozen=True, slots=True)
class ComplexityRecord:
    """Complexity accounting for a candidate representation."""

    candidate_id: str
    added_components: int
    expression_complexity: float
    search_cost: float
    description_length: float


@dataclass(frozen=True, slots=True)
class DiscoveryEvaluation:
    """Complete evaluation record for one candidate."""

    candidate_id: str
    evaluations: Sequence[EvaluationRecord]
    falsification: Sequence[FalsificationRecord]
    interventions: Sequence[InterventionRecord]
    transfer: Sequence[TransferRecord]
    representation_recovery: RepresentationRecoveryRecord
    complexity: ComplexityRecord
    outcome: DiscoveryOutcome
    evaluator_metadata: Mapping[str, str | int | float | bool]