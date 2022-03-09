from __future__ import annotations

from enum import Enum
from typing import Optional


class ValueDomain(Enum):
    """Class representing the value domain, so which domain the question is about.
    ADMINISTERED_VACCINES: The question is about vaccine doses that have been administered.
    VACCINATED_PEOPLE: The question is about people that have been vaccinated.
    POSITIVE_CASES: The question is about positive covid tests.
    UNKNOWN: The value domain is unknown.
    """
    ADMINISTERED_VACCINES = 1
    VACCINATED_PEOPLE = 2
    POSITIVE_CASES = 3
    UNKNOWN = 4

    @staticmethod
    def from_str(value_domain: str) -> Optional[ValueDomain]:
        try:
            return ValueDomain[value_domain.upper()]
        except KeyError:
            return ValueDomain["UNKNOWN"]
