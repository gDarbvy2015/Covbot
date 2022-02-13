from typing import Any

from lib.database.querier import Querier
from lib.intention.intent import Intent
from lib.intention.intent_recognizer import IntentRecognizer


class AnswerGenerator:
    def __init__(self):
        pass

    def generate_answer(self, intent: Intent, result: Any) -> str:
        result = result[0]
        answer = "On {date}, **{cases}** have been reported in {country}.".format(
            date=f"{result.date:%B %d, %Y}",
            cases=result.cases,
            country=result.country
        )

        return answer


if __name__ == '__main__':
    sent = "How many people were infected on November 27th 2021 in Austria?"
    ir = IntentRecognizer()
    querier = Querier()
    answer_generator = AnswerGenerator()

    intent = ir.get_intent(sent)
    result = querier.get_results(intent)
    answer = answer_generator.generate_answer(intent, result)
    print(answer)
