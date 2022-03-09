""" Setup script

This script will download any additional necessary dependencies and set up the database to run the other
parts of the chatbot.

"""

import nltk
from spacy.cli import download as spacy_download

spacy_download('en_core_web_lg')
nltk.download('punkt')
