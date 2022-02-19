import spacy
from nltk import PorterStemmer

from lib.spacy_components.spacy import get_spacy

nlp = get_spacy()
print(nlp.pipe_names)
stemmer = PorterStemmer()

sent1 = "How many new cases have been reported in Austria?"
sent2 = "How many new people have moved to Austria and what is the infection?"
sent3 = "How many new super interesting people are there?"
sent4 = "How many new COVID cases are there in the UK?"
sentences = [sent4]

# for sentence in sentences:
#     doc = nlp(sentence)
#     relevant = False
#     for token in doc:
#         if token.lower_ == "how":
#             if token.head.lower_ == "many":
#                 if token.head.head.lemma_ in ["infect", "case"]:
#                     relevant = True
#     print(relevant)
#
#     print("_____________")

sent5 = "How many new cases have been reported in Austria before September the 25th 2021?"
sentences = [sent5]

for sentence in sentences:
    doc = nlp(sentence)
    for token in doc:
        print(f"TOKEN: {token.text}, POS: {token.pos_}")
        print(f"DEP: {token.dep_}, HEAD: {token.head}")
        print("---------------------")



from spacy.matcher import DependencyMatcher

pattern =[
{
        "RIGHT_ID": "how_pat",
        "RIGHT_ATTRS": {
            "LEMMA": "how"
        }
},
{
    "LEFT_ID": "how_pat",
    "REL_OP": "<",
    "RIGHT_ID": "how_many_pat",
    "RIGHT_ATTRS": {
        "LEMMA": "many"
    }
},
{
        "LEFT_ID": "how_many_pat",
        "REL_OP": "<<",
        "RIGHT_ID": "numper_pat",
        "RIGHT_ATTRS": {
            "_": {
                "stem": {
                    "IN": ["case", "test"]
                }
            }
        }
}
]

sent = nlp("How many positive cases were there in Austria and how many negative tests were there?")
matcher = DependencyMatcher(nlp.vocab)
matcher.add("NUMBER", [pattern])
matches = matcher(sent)

print(matches)