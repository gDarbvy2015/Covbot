import spacy
from nltk import PorterStemmer

nlp = spacy.load("en_core_web_sm")
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

sent5 = "How many people have tested positive for COVID in Germany today?"
sentences = [sent5]

for sentence in sentences:
    doc = nlp(sentence)
    for token in doc:
        print(f"{token.text}, {list(token.children)}")