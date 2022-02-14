from __future__ import annotations
from enum import Enum


class Intent(Enum):
    UNKNOWN = 1
    NUMBER_OF_POSITIVE_CASES = 2
    NUMBER_OF_ADMINISTERED_VACCINES = 3

    @staticmethod
    def from_str(topic_string: str) -> Intent:
        if topic_string.lower() == "number_of_positive_cases":
            return Intent.NUMBER_OF_POSITIVE_CASES
        elif topic_string.lower() == "number_of_administered_vaccines":
            return Intent.NUMBER_OF_ADMINISTERED_VACCINES
        else:
            return Intent.UNKNOWN
