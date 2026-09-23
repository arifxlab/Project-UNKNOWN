"""Public runtime boundary for Project UNKNOWN.

This module exposes the environment interface available to UNKNOWN.

Scientific boundary
-------------------
The runtime deliberately exposes only public schemas. Hidden benchmark
truth and evaluation records remain outside this interface.

The initial implementation provides deterministic environment mechanics
without yet implementing the full synthetic benchmark dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass

from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
    ObservationKind,
    PublicAction,
    PublicEnvironmentConfig,
    PublicEnvironmentMetadata,
    PublicIntervention,
    PublicObservation,
    PublicStepResult,
)


class EnvironmentRuntimeError(RuntimeError):
    """Base error for public environment runtime failures."""


class EnvironmentNotInitializedError(EnvironmentRuntimeError):
    """Raised when the environment is used before reset."""


class EnvironmentTerminalError(EnvironmentRuntimeError):
    """Raised when an operation is attempted after termination."""


class InvalidPublicActionError(EnvironmentRuntimeError):
    """Raised when a public action is invalid for the current environment."""


class InvalidPublicInterventionError(EnvironmentRuntimeError):
    """Raised when a public intervention is invalid for the environment."""


@dataclass(slots=True)
class _PublicRuntimeState:
    """Internal runtime state containing only public simulation state."""

    experiment_id: str
    step_index: int
    entities: tuple
    terminal: bool


class PublicEnvironmentRuntime:
    """Public environment runtime exposed to UNKNOWN.

    The runtime owns public state and exposes only public schema objects.

    Hidden benchmark truth must not be stored in this object.
    Evaluation state must not be stored in this object.
    """

    def __init__(self) -> None:
        self._config: PublicEnvironmentConfig | None = None
        self._state: _PublicRuntimeState | None = None

    def reset(
        self,
        config: PublicEnvironmentConfig,
        seed: int,
    ) -> PublicObservation:
        """Initialize a deterministic public environment episode.

        The seed is accepted as part of the reproducibility contract. The
        initial runtime shell does not yet use stochastic dynamics.
        """
        del seed

        if config.max_steps <= 0:
            raise ValueError("max_steps must be greater than zero.")

        if config.world_width <= 0:
            raise ValueError("world_width must be greater than zero.")

        if config.world_height <= 0:
            raise ValueError("world_height must be greater than zero.")

        if config.entity_count < 0:
            raise ValueError("entity_count cannot be negative.")

        if config.observation_history_limit <= 0:
            raise ValueError(
                "observation_history_limit must be greater than zero."
            )

        self._config = config

        self._state = _PublicRuntimeState(
            experiment_id="opaque-experiment-001",
            step_index=0,
            entities=(),
            terminal=False,
        )

        return self.observe()

    def observe(self) -> PublicObservation:
        """Return the current public observation."""
        state = self._require_initialized()

        return PublicObservation(
            observation_id=f"observation-{state.step_index:06d}",
            step_index=state.step_index,
            kind=ObservationKind.STATE,
            entities=state.entities,
            relations=(),
            events=(),
            timestamp=state.step_index,
        )

    def step(self, action: PublicAction) -> PublicStepResult:
        """Apply one public action and return the resulting observation."""
        state = self._require_initialized()

        if state.terminal:
            raise EnvironmentTerminalError(
                "Cannot step an environment that is already terminal."
            )

        self._validate_action(action)

        assert self._config is not None

        next_step = state.step_index + 1
        terminal = next_step >= self._config.max_steps

        self._state = _PublicRuntimeState(
            experiment_id=state.experiment_id,
            step_index=next_step,
            entities=state.entities,
            terminal=terminal,
        )

        return PublicStepResult(
            observation=self.observe(),
            reward=0.0,
            terminal=terminal,
        )

    def intervene(
        self,
        intervention: PublicIntervention,
    ) -> PublicStepResult:
        """Apply one public intervention.

        The initial runtime shell validates the intervention contract but
        does not yet implement benchmark dynamics.
        """
        state = self._require_initialized()

        if state.terminal:
            raise EnvironmentTerminalError(
                "Cannot intervene in an environment that is already terminal."
            )

        self._validate_intervention(intervention)

        assert self._config is not None

        next_step = state.step_index + 1
        terminal = next_step >= self._config.max_steps

        self._state = _PublicRuntimeState(
            experiment_id=state.experiment_id,
            step_index=next_step,
            entities=state.entities,
            terminal=terminal,
        )

        return PublicStepResult(
            observation=self.observe(),
            reward=0.0,
            terminal=terminal,
        )

    def is_terminal(self) -> bool:
        """Return whether the current public episode has terminated."""
        state = self._require_initialized()
        return state.terminal

    def episode_metadata(self) -> PublicEnvironmentMetadata:
        """Return public operational metadata for the current episode."""
        self._require_initialized()
        assert self._config is not None
        assert self._state is not None

        return PublicEnvironmentMetadata(
            experiment_id=self._state.experiment_id,
            environment_version=self._config.environment_version,
            schema_version=self._config.schema_version,
            max_steps=self._config.max_steps,
            action_kinds=self._config.allowed_action_kinds,
            intervention_kinds=self._config.allowed_intervention_kinds,
        )

    def _require_initialized(self) -> _PublicRuntimeState:
        """Return runtime state or raise if reset has not occurred."""
        if self._state is None:
            raise EnvironmentNotInitializedError(
                "Environment must be reset before use."
            )

        return self._state

    def _validate_action(self, action: PublicAction) -> None:
        """Validate an action against the public configuration."""
        assert self._config is not None

        if action.kind not in self._config.allowed_action_kinds:
            raise InvalidPublicActionError(
                f"Action kind {action.kind!r} is not allowed."
            )

        if action.kind is ActionKind.MOVE and action.vector is None:
            raise InvalidPublicActionError(
                "MOVE actions require a public vector."
            )

    def _validate_intervention(
        self,
        intervention: PublicIntervention,
    ) -> None:
        """Validate an intervention against the public configuration."""
        assert self._config is not None

        if intervention.kind not in self._config.allowed_intervention_kinds:
            raise InvalidPublicInterventionError(
                f"Intervention kind {intervention.kind!r} is not allowed."
            )

        if (
            intervention.kind
            in {
                InterventionKind.SET_POSITION,
                InterventionKind.SET_VELOCITY,
            }
            and intervention.vector is None
        ):
            raise InvalidPublicInterventionError(
                f"{intervention.kind.value} interventions require a vector."
            )