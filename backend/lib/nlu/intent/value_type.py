from __future__ import annotations

from enum import Enum
from typing import Optional


class ValueType(Enum):
    """Class representing the value type, so what kind of value we are trying to extract.
    NUMBER: When trying to extract a number, such as the number of positive cases on a day or the highest number
    of vaccines administered on a certain day.
    DAY: When we are trying to extract a day - for example "When was the highest number of cases recorded in Austria?".
    LOCATION: When we are trying to extract a location - for example "Where was the lowest number of cases reported?".
    UNKNOWN: When the value type is unknown.
    """
    NUMBER = 1
    DAY = 2
    LOCATION = 3
    UNKNOWN = 4

    @staticmethod
    def from_str(value_type: str) -> Optional[ValueType]:
        try:
            return ValueType[value_type.upper()]
        except KeyError:
            return ValueType["UNKNOWN"]
