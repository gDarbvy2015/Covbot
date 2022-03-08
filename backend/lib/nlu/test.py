import json

import requests

# from sutime import SUTime

# sutime = SUTime(mark_time_ranges=True, include_range=True)
from lib.nlu.patterns import Pattern
from lib.spacy_components.custom_spacy import CustomSpacy

text = "How many people got the COVID vaccine"

spacy = CustomSpacy.get_spacy()

span = spacy(text)[:]

for token in span:
    print(token, " ", token.dep_)


print(Pattern.has_valid_pattern(span, [Pattern.covid_vaccine_pattern, Pattern.covid_pattern]))