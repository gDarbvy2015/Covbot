from __future__ import annotations

from enum import Enum
from typing import Optional


class MeasurementType(Enum):
    """Class representing the measurement type, so whether we are trying to access a daily
    value or a cumulative value.
    DAILY: If we are trying to access a daily value.
    CUMULATIVE: If we are trying to access a cumulative value.
    UNKNOWN: Unknown measurement type.
    """
    DAILY = 1
    CUMULATIVE = 2
    UNKNOWN = 3

    @staticmethod
    def from_str(measurement_type: str) -> Optional[MeasurementType]:
        """Convert a string to a MeasurementType."""
        try:
            return MeasurementType[measurement_type.upper()]
        except KeyError:
            return MeasurementType["UNKNOWN"]
