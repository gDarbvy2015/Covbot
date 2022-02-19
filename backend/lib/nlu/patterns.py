from typing import List

from nltk import PorterStemmer

from lib.nlu.topic import TopicRecognizer

stemmer = PorterStemmer()
topic_recognizer = TopicRecognizer()

people_trigger_words = [stemmer.stem(word)
                        for word in ["human", "people", "person", "individual"]]

human_pattern: List[dict] = [{
    "RIGHT_ID": "human_pattern",
    "RIGHT_ATTRS": {
        "_": {
            "stem": {
                "IN": people_trigger_words
            }
        }
    }
}]

vaccine_trigger_pattern: List[dict] = [{
    "RIGHT_ID": "vaccine_trigger_pattern",
    "RIGHT_ATTRS": {
        "_": {
            "stem": {
                "IN": list(topic_recognizer.get_vaccine_trigger_words())
            }
        }
    }
}]

case_trigger_pattern: List[dict] = [{
    "RIGHT_ID": "case_trigger_pattern",
    "RIGHT_ATTRS": {
        "_": {
            "stem": {
                "IN": list(topic_recognizer.get_cases_trigger_words())
            }
        }
    }
}]

how_many_pattern: List[dict] = [{
    "RIGHT_ID": "how_pattern",
    "RIGHT_ATTRS": {
        "LEMMA": "how"
    }
},
    {
        "LEFT_ID": "how_pattern",
        "REL_OP": "<",
        "RIGHT_ID": "how_many_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": "many"
        }
    }]

number_of_pattern: List[dict] = [{
    "RIGHT_ID": "number_pattern",
    "RIGHT_ATTRS": {
        "LEMMA": "number"
    }
},
    {
        "LEFT_ID": "number_pattern",
        "REL_OP": "<",
        "RIGHT_ID": "number_of_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": "of"
        }
}]