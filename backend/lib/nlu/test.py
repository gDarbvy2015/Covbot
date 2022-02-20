from spacy.matcher import DependencyMatcher

from lib.spacy_components.spacy import get_spacy
from lib.nlu.patterns import human_pattern, how_many_pattern, vaccine_trigger_pattern, case_trigger_pattern, \
    what_country_pattern, what_pattern, country_pattern


nlp = get_spacy()
sent = nlp("Which country has had the most corona cases?")


matcher = DependencyMatcher(nlp.vocab)

matcher.add("case", [what_pattern, country_pattern])

result = matcher(sent)

print(matcher(sent))