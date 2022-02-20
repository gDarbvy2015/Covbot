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

country_pattern: List[dict] = [{
    "RIGHT_ID": "country_pattern",
    "RIGHT_ATTRS": {
        "LEMMA": {
            "IN": ["country", "nation"]
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

how_pattern: List[dict] = [
{
    "RIGHT_ID": "how_pattern",
    "RIGHT_ATTRS": {
        "LEMMA": "how"
    }
    }
]

how_many_pattern: List[dict] = how_pattern + [
    {
        "LEFT_ID": "how_pattern",
        "REL_OP": "<",
        "RIGHT_ID": "how_many_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": "many"
        }
    }]

what_pattern: List[dict] = [
    {
        "RIGHT_ID": "what_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": {
                "IN": ["which", "what"]
            }
        }
    }
]

what_day_pattern: List[dict] = what_pattern + [
    {
        "LEFT_ID": "what_pattern",
        "REL_OP": "<<",
        "RIGHT_ID": "what_day_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": {
                "IN": ["day", "time", "date"]
            }
        }
    }
]

what_country_pattern: List[dict] = what_pattern + [
    {
        "LEFT_ID": "what_pattern",
        "REL_OP": "<<",
        **country_pattern[0]
    }
]

what_is_country_pattern: List[dict] = what_pattern + [
    {
        "LEFT_ID": "what_pattern",
        "REL_OP": "$++",
        **country_pattern[0]
    }
]

when_pattern: List[dict] = [
    {
        "RIGHT_ID": "when_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": "when"
        }
    }
]

where_pattern: List[dict] = [
    {
        "RIGHT_ID": "where_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": "where"
        }
    }
]

number_of_pattern: List[dict] = [{
    "RIGHT_ID": "number_pattern",
    "RIGHT_ATTRS": {
        "LEMMA": {
            "IN": ["amount", "number"]
        }
    }
},
    {
        "LEFT_ID": "number_pattern",
        "REL_OP": ">",
        "RIGHT_ID": "number_of_pattern",
        "RIGHT_ATTRS": {
            "LEMMA": "of"
        }
    }]
