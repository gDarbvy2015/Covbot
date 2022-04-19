from __future__ import annotations

import json
import re
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, List

import requests
from dateutil.parser import parse
from spacy.tokens import Span


@dataclass
class Date:
    """Class representing a date with additional information.
    type: Considered timeframe, can be "DAY", "WEEK", "MONTH", "YEAR"
    value: The actual value of the date as a datetime.date object. In case of a week, month or year, it will
    always be the first day of that time period.
    text: The text from which the date was extracted.
    """
    type: str
    value: datetime.date
    text: Optional[str]

    @staticmethod
    def generate_date_message(date: Date, today: datetime.date = None, include_preposition = True) -> str:
        """Generates a string representation of a date taking into consideration the timeframe."""

        if today is None:
            today = datetime.now().date()

        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        def custom_strftime(format, t):
            return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

        preposition: str = "on " if include_preposition else ""

        if date.type == "DAY":
            difference: timedelta = today - date.value
            if difference >= timedelta(days=0):
                if difference == timedelta(days=0):
                    return "today"
                if difference == timedelta(days=1):
                    return "yesterday"
                elif difference <= timedelta(days=5):
                    return f"{difference.days} days ago"
                else:
                    return custom_strftime(preposition + "%B {S} %Y", date.value)
            else:
                if difference == timedelta(days=-1):
                    return "tomorrow"
                else:
                    return custom_strftime(preposition + "%B {S} %Y", date.value)
        elif date.type == "WEEK":
            today_iso = today.isocalendar()
            date_iso = date.value.isocalendar()
            date_start = date.value - timedelta(days=date.value.weekday())
            date_end = date_start + timedelta(days=6)
            preposition: str = "in " if include_preposition else ""

            if today_iso[0] == date_iso[0]:
                if today_iso[1] == date_iso[1]:
                    return "this week"
                elif today_iso[1] - date_iso[1] == 1:
                    return "last week"
                elif date_iso[1] - today_iso[1] == 1:
                    return "next week"
                else:
                    return preposition + f"the week from the {custom_strftime('{S} of %B %Y', date_start)} to the " \
                           f"{custom_strftime('{S} of %B %Y', date_end)}"
            else:
                return preposition + f"the week from the {custom_strftime('{S} of %B %Y', date_start)} to the " \
                       f"{custom_strftime('{S} of %B %Y', date_end)}"
        elif date.type == "MONTH":
            preposition: str = "in " if include_preposition else ""
            if today.year == date.value.year:
                if today.month == date.value.month:
                    return "this month"
                elif today.month == date.value.month - 1:
                    return "next month"
                elif today.month == date.value.month + 1:
                    return "last month"
                else:
                    return preposition + f"{custom_strftime('%B %Y', date.value)}"
            else:
                return f"in {custom_strftime('%B %Y', date.value)}"
        elif date.type == "YEAR":
            preposition: str = "in " if include_preposition else ""
            if today.year == date.value.year:
                return "this year"
            elif today.year == date.value.year + 1:
                return "last year"
            elif today.year == date.value.year - 1:
                return "next year"
            else:
                return preposition + f"{date.value.year}"
        else:
            raise NotImplementedError()

    def __str__(self):
        return Date.generate_date_message(Date(self.type, self.value, self.text))


class DateRecognizer:
    """Class providing helper methods to recognize dates in text."""
    def recognize_date(self, span: Span) -> Optional[Date]:
        """Extracts the first date in a span."""
        result: List[dict] = self._send_request(str(span))
        if len(result) > 0:
            if result[0]["value"] == "P1D":
                return None
            else:
                return self._parse_date(result[0])
        else:
            return None

    def _parse_date(self, date_dict: dict) -> Optional[Date]:
        """Converts the date representation from the Stanford parser to a Date object."""
        if re.match(r"^\d{4}$", date_dict["value"]):
            return Date("YEAR", parse(date_dict["value"]).date(), date_dict["text"])
        elif re.match(r"^\d{4}-\d{2}$", date_dict["value"]):
            return Date("MONTH", parse(date_dict["value"]).date(), date_dict["text"])
        elif re.match(r"^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2})?$", date_dict["value"]):
            return Date("DAY", parse(date_dict["value"]).date(), date_dict["text"])
        elif re.match(r"^\d{4}-W\d{2}$", date_dict["value"]):
            return Date("WEEK", datetime.strptime(date_dict["value"] + ' 1', "%Y-W%W %w").date(), date_dict["text"])
        return None

    def _send_request(self, sentence: str) -> List[dict]:
        """Sends a request to the server running the Stanford parser and returns the result as a dict."""
        properties: dict = {
            "date": datetime.now().isoformat(),
            "annotators": "tokenize, ssplit, pos, lemma, ner",
            "outputFormat": "json",
        }
        res: dict = requests.post(f'http://corenlp:9000/?properties={json.dumps(properties)}',
                                  data={'data': sentence}).json()

        dates = list()
        for sentence in res["sentences"]:
            if "entitymentions" in sentence:
                for entity in sentence["entitymentions"]:
                    if entity["ner"] in ["DATE", "TIME"] and "timex" in entity and "value" in entity["timex"]:
                        print(entity)
                        dates.append({
                            "text": entity["text"],
                            "type": "DATE",
                            "value": entity["timex"]["value"]
                        })

        return dates
