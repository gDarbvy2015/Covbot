from dataclasses import dataclass
from typing import Optional

from spacy.tokens import Span

from lib.nlu.slot.date import Date, DateRecognizer
from lib.nlu.slot.location import LocationRecognizer


@dataclass
class Slots:
    date: Optional[Date]
    location: Optional[str]


class SlotsFiller:
    def __init__(self):
        self._date_recognizer = DateRecognizer()
        self._location_recognizer = LocationRecognizer()

    def fill_slots(self, span: Span) -> Slots:
        date = self._date_recognizer.recognize_date(span)
        location = self._location_recognizer.recognize_location(span)

        return Slots(date, location)
