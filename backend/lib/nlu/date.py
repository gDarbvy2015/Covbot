from dataclasses import dataclass
from typing import Optional

from sutime import SUTime


@dataclass
class Date:
    type: str
    original_string: str
    value_string: str


class DateRecognizer:
    def __init__(self):
        self.sutime = SUTime(mark_time_ranges=True, include_range=True)

    def recognize_date(self, sentence: str) -> Optional[Date]:
        result = self.sutime.parse(sentence)
        if len(result) > 0:
            return Date(result[0]["type"], result[0]["text"], result[0]["value"])
        else:
            return None


recognizer = DateRecognizer()
recognizer.recognize_date("This is my favorite thing at November 3rd, 2021")
