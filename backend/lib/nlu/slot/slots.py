from dataclasses import dataclass
from typing import Optional

from spacy.tokens import Span

from lib.nlu.slot.date import Date, DateRecognizer
from lib.nlu.slot.location import LocationRecognizer


@dataclass
class Slots:
    """Class representing the slots of a query.
    date: The date mentioned in the query.
    location: The location mentioned in the query.
    """
    date: Optional[Date]
    location: Optional[str]


class SlotsFiller:
    """Class providing helper slots to extract the slots from text."""
    def __init__(self):
        self._date_recognizer = DateRecognizer()
        self._location_recognizer = LocationRecognizer()

    def fill_slots(self, span: Span) -> Slots:
        """Returns the filled slots for a span."""
        date = self._date_recognizer.recognize_date(span)
        location = self._location_recognizer.recognize_location(span)

        return Slots(date, location)
