"""Public runtime boundary for Project UNKNOWN.

This module exposes the environment interface available to UNKNOWN.

Scientific boundary
-------------------
The runtime exposes only public schemas.

Internal deterministic world state remains behind the observation projector.
Hidden benchmark truth and evaluation records remain outside this interface.

Architecture
------------
    PublicEnvironmentRuntime
            |
            v
    DeterministicWorld
            |
            v
        WorldState
            |
            v
    PublicObservationProjector
            |
            v
      PublicObservation

The runtime never returns WorldState directly.
"""

from __future__ import annotations

from dataclasses import dataclass

from unknown.environment.dynamics import (
    DeterministicWorld,
    InvalidWorldActionError,
    WorldNotInitializedError,
    WorldState,
    WorldTerminalError,
)
from unknown.environment.observation import PublicObservationProjector
from unknown.environment.schemas.public import (
    ActionKind,
    InterventionKind,
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
    """Internal runtime control state.

    This object contains only runtime control information.

    The actual simulation state is owned by DeterministicWorld.
    """

    experiment_id: str
    terminal: bool


class PublicEnvironmentRuntime:
    """Public environment runtime exposed to UNKNOWN.

    The runtime owns the deterministic world and observation projector.

    Scientific boundary
    -------------------
    The runtime must not contain:

    - hidden benchmark truth
    - evaluation state
    - ground-truth representations
    - oracle outcomes
    - benchmark condition labels

    Internal WorldState is never returned through the public API.
    """

    def __init__(self) -> None:
        self._config: PublicEnvironmentConfig | None = None
        self._state: _PublicRuntimeState | None = None
        self._world = DeterministicWorld()
        self._projector = PublicObservationProjector()

    def reset(
        self,
        config: PublicEnvironmentConfig,
        seed: int,
    ) -> PublicObservation:
        """Initialize a deterministic environment episode.

        The deterministic world owns the actual simulation state.
        The returned observation is produced exclusively through the public
        observation projector.
        """

        self._validate_config(config)

        try:
            self._world.reset(config=config, seed=seed)
        except ValueError:
            raise
        except Exception as error:
            raise EnvironmentRuntimeError(
                "Unable to initialize the environment."
            ) from error

        self._config = config

        self._state = _PublicRuntimeState(
            experiment_id="opaque-experiment-001",
            terminal=False,
        )

        return self.observe()

    def observe(self) -> PublicObservation:
        """Return the current public observation."""

        self._require_initialized()

        return self._project_current_world()

    def step(self, action: PublicAction) -> PublicStepResult:
        """Apply one public action and return the resulting observation."""

        runtime_state = self._require_initialized()

        if runtime_state.terminal:
            raise EnvironmentTerminalError(
                "Cannot step an environment that is already terminal."
            )

        self._validate_action(action)

        world_action = self._to_world_action(action)

        try:
            world_state = self._world.step(world_action)
        except WorldTerminalError as error:
            raise EnvironmentTerminalError(
                "Cannot step an environment that is already terminal."
            ) from error
        except InvalidWorldActionError as error:
            raise InvalidPublicActionError(
                "The public action was rejected by the environment."
            ) from error
        except WorldNotInitializedError as error:
            raise EnvironmentNotInitializedError(
                "Environment must be reset before use."
            ) from error

        terminal = self._world.is_terminal()

        self._state = _PublicRuntimeState(
            experiment_id=runtime_state.experiment_id,
            terminal=terminal,
        )

        return PublicStepResult(
            observation=self._project_world_state(world_state),
            reward=0.0,
            terminal=terminal,
        )

    def intervene(
        self,
        intervention: PublicIntervention,
    ) -> PublicStepResult:
        """Validate a public intervention.

        Intervention transition dynamics are intentionally not implemented
        in DeterministicWorld yet.

        This method therefore preserves the existing public contract without
        inventing a second transition mechanism inside the runtime.
        """

        state = self._require_initialized()

        if state.terminal:
            raise EnvironmentTerminalError(
                "Cannot intervene in an environment that is already terminal."
            )

        self._validate_intervention(intervention)

        raise NotImplementedError(
            "Intervention transition dynamics are not implemented yet."
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

    def _project_current_world(self) -> PublicObservation:
        """Project the current world state into the public schema."""

        try:
            world_state = self._world.state()
        except WorldNotInitializedError as error:
            raise EnvironmentNotInitializedError(
                "Environment must be reset before use."
            ) from error

        return self._project_world_state(world_state)

    def _project_world_state(
        self,
        world_state: WorldState,
    ) -> PublicObservation:
        """Project an internal world state through the public boundary."""

        return self._projector.project(world_state)

    def _require_initialized(self) -> _PublicRuntimeState:
        """Return runtime control state or raise if reset has not occurred."""

        if self._state is None:
            raise EnvironmentNotInitializedError(
                "Environment must be reset before use."
            )

        return self._state

    @staticmethod
    def _validate_config(config: PublicEnvironmentConfig) -> None:
        """Validate public environment configuration."""

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

    def _validate_action(self, action: PublicAction) -> None:
        """Validate an action against the public configuration."""

        assert self._config is not None

        if action.kind not in self._config.allowed_action_kinds:
            raise InvalidPublicActionError(
                f"Action kind {action.kind!r} is not allowed."
            )

        if action.kind is ActionKind.NO_OP:
            if action.entity_id is not None or action.vector is not None:
                raise InvalidPublicActionError(
                    "NO_OP actions cannot specify an entity or vector."
                )

        elif action.kind is ActionKind.MOVE:
            if action.entity_id is None:
                raise InvalidPublicActionError(
                    "MOVE actions require an entity identifier."
                )

            if action.vector is None:
                raise InvalidPublicActionError(
                    "MOVE actions require a public vector."
                )

        elif action.kind is ActionKind.INTERACT:
            if action.entity_id is None:
                raise InvalidPublicActionError(
                    "INTERACT actions require an entity identifier."
                )

    @staticmethod
    def _to_world_action(action: PublicAction) -> PublicAction:
        """Return the public action accepted by the dynamics layer."""

        return action

    def _validate_intervention(
        self,
        intervention: PublicIntervention,
    ) -> None:
        """Validate an intervention against public configuration."""

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