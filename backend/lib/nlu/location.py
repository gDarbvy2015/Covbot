from typing import Optional

from spacy.tokens import Doc


class LocationRecognizer:
    def recognize_location(self, doc: Doc) -> Optional[str]:
        location_ents = [ent.text for ent in doc.ents
                         if ent.label_ == "GPE"]
        if len(location_ents) == 0:
            return None
        else:
            return location_ents[0]
