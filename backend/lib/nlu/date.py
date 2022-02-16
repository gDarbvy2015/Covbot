from datetime import datetime
from dataclasses import dataclass
from typing import Optional, Union
import re
from dateutil.parser import parse

from sutime import SUTime


@dataclass
class Date:
    type: str
    original_string: str
    value_string: str
    value: dict


class DateRecognizer:
    def __init__(self):
        self.sutime = SUTime(mark_time_ranges=True, include_range=True)

    def recognize_date(self, sentence: str) -> Optional[Date]:
        result = self.sutime.parse(sentence)
        if len(result) > 0:
            if result[0]["value"] == "P1D":
                return None
            else:
                return Date(result[0]["type"], result[0]["text"], result[0]["value"], self._parse_date(result[0]["value"]))
        else:
            return None

    def _parse_date(self, date_string: str) -> Optional[dict]:
        if re.match(r"^\d{4}$", date_string):
            return {"time": "YEAR", "value": parse(date_string)}
        elif re.match(r"^\d{4}-\d{2}$", date_string):
            return {"time": "MONTH", "value": parse(date_string)}
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", date_string):
            return {"time": "DAY", "value": parse(date_string)}
        elif re.match(r"^\d{4}-W\d{2}$", date_string):
            return {"time": "WEEK", "value": datetime.strptime(date_string + ' 1', "%Y-W%W %w")}

        return None


recognizer = DateRecognizer()
recognizer.recognize_date("This is my favorite thing at November 3rd, 2021")
