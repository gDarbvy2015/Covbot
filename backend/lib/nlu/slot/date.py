import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
import re

import requests
from dateutil.parser import parse
from spacy.tokens import Span


@dataclass
class Date:
    type: str
    original_string: str
    value_string: str
    value: dict


class DateRecognizer:
    def recognize_date(self, span: Span) -> Optional[Date]:
        result = self._send_request(str(span))
        if len(result) > 0:
            if result[0]["value"] == "P1D":
                return None
            else:
                return Date(result[0]["type"], result[0]["text"], result[0]["value"], self._parse_date(result[0]["value"]))
        else:
            return None

    def _parse_date(self, date_string: str) -> Optional[dict]:
        if re.match(r"^\d{4}$", date_string):
            return {"time": "YEAR", "value": parse(date_string).date()}
        elif re.match(r"^\d{4}-\d{2}$", date_string):
            return {"time": "MONTH", "value": parse(date_string).date()}
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", date_string):
            return {"time": "DAY", "value": parse(date_string).date()}
        elif re.match(r"^\d{4}-W\d{2}$", date_string):
            return {"time": "WEEK", "value": datetime.strptime(date_string + ' 1', "%Y-W%W %w").date()}

        return None

    def _send_request(self, sentence: str) -> List[dict]:
        properties = {
            "date": datetime.now().isoformat(),
            "annotators": "tokenize, ssplit, pos, lemma, ner",
            "outputFormat": "json",
            "sutime.includeRange": "true",
            "sutime.markTimeRanges": "true",
        }

        res = requests.post(f'http://localhost:9000/?properties={json.dumps(properties)}',
                            data={
                                'data': sentence}).json()

        dates = list()
        print(res)
        for sentence in res["sentences"]:
            if "entitymentions" in sentence:
                for entity in sentence["entitymentions"]:
                    if entity["ner"] == "DATE":
                        dates.append({
                            "text": entity["text"],
                            "type": entity["ner"],
                            "value": entity["timex"]["value"]
                        })

        return dates


if __name__ == '__main__':
    recognizer = DateRecognizer()
    print(recognizer.recognize_date("I had to do it last week."))
