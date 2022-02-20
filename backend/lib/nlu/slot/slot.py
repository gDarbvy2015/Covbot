from dataclasses import dataclass

from spacy.tokens import Span

from lib.nlu.slot.date import Date, DateRecognizer
from lib.nlu.slot.location import LocationRecognizer


@dataclass
class Slot:
    date: Date
    location: str


class SlotFiller:
    def __init__(self):
        self.date_recognizer = DateRecognizer()
        self.location_recognizer = LocationRecognizer()

    def fill_slots(self, span: Span) -> Slot:
        date = self.date_recognizer.recognize_date(span)
        location = self.location_recognizer.recognize_location(span)

        return Slot(date, location)
