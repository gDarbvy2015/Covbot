""" Setup script

This script will download any additional necessary dependencies to run the other
parts of the program.

"""

import nltk
from spacy.cli import download as spacy_download

spacy_download('en')
nltk.download('punkt')
