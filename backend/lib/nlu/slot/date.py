import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List
import re

import requests
from dateutil.parser import parse
from requests import Response
from spacy.tokens import Span


@dataclass
class Date:
    type: str
    value: datetime.date
    text: Optional[str]


class DateRecognizer:
    def recognize_date(self, span: Span) -> Optional[Date]:
        result: List[dict] = self._send_request(str(span))
        if len(result) > 0:
            if result[0]["value"] == "P1D":
                return None
            else:
                return self._parse_date(result[0])
        else:
            return None

    def _parse_date(self, date_dict: dict) -> Optional[Date]:
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
        properties: dict = {
            "date": datetime.now().isoformat(),
            "annotators": "tokenize, ssplit, pos, lemma, ner",
            "outputFormat": "json",
        }

        res: dict = requests.post(f'http://localhost:9000/?properties={json.dumps(properties)}',
                            data={
                                'data': sentence}).json()

        dates = list()
        for sentence in res["sentences"]:
            if "entitymentions" in sentence:
                for entity in sentence["entitymentions"]:
                    if entity["ner"] in["DATE", "TIME"]:
                        dates.append({
                            "text": entity["text"],
                            "type": "DATE",
                            "value": entity["timex"]["value"]
                        })

        return dates


if __name__ == '__main__':
    recognizer = DateRecognizer()
    print(recognizer.recognize_date("How many positive cases were there in Germany yesterday?"))
