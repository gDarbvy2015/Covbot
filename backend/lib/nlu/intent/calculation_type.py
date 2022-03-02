from __future__ import annotations

from enum import Enum
from typing import Optional


class CalculationType(Enum):
    RAW_VALUE = 1
    SUM = 2
    MAXIMUM = 3
    MINIMUM = 4
    UNKNOWN = 5

    @staticmethod
    def from_str(calculation_type: str) -> Optional[CalculationType]:
        try:
            return CalculationType[calculation_type.upper()]
        except KeyError:
            return CalculationType["UNKNOWN"]