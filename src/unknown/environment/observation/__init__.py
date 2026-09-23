"""Public observation projection for Project UNKNOWN.

This package contains the boundary that projects internal world state into
the information legitimately observable by the UNKNOWN discovery system.
"""

from unknown.environment.observation.projection import (
    ObservationProjectionError,
    PublicObservationProjector,
)

__all__ = [
    "ObservationProjectionError",
    "PublicObservationProjector",
]