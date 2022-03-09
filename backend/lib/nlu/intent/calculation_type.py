from __future__ import annotations

from enum import Enum
from typing import Optional


class CalculationType(Enum):
    """Class representing the calculation type, so what type of value is supposed to be calculated.
    RAW_VALUE: Takes a raw value from a row in the database. For example, when asking "How many cases were there today
    in Austria?", we want the raw number of daily cases from today from Austria in the database.
    SUM: Requires us to calculate a sum, for example when asking "How many cases were there this week in Austria?",
    we need to sum all the daily values for this week.
    MAXIMUM: If we are trying to find the highest value, e.g. "What was the highest number of cases detected in Austria
    this year?".
    MAXIMUM: If we are trying to find the highest value, e.g. "What was the lowest number of cases detected in Austria
    this year?".
    UNKNOWN: Unknown calculation type.
    """
    RAW_VALUE = 1
    SUM = 2
    MAXIMUM = 3
    MINIMUM = 4
    UNKNOWN = 5

    @staticmethod
    def from_str(calculation_type: str) -> Optional[CalculationType]:
        """Convert a string to a CalculationType."""
        try:
            return CalculationType[calculation_type.upper()]
        except KeyError:
            return CalculationType["UNKNOWN"]
