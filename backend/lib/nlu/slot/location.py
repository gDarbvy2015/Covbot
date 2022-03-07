import re
from typing import Optional, List, Set

from spacy.tokens import Span

class Location:
    _countries: Set[str] = {'micronesia', 'poland', 'philippines', 'portugal', 'anguilla', 'niue', 'moldova', 'bermuda', 'canada',
              'tonga', 'aruba', 'angola', 'ireland', 'ecuador', 'timor', 'afghanistan', 'iraq',
              'hong kong', 'liechtenstein', 'maldives', 'palau', 'benin', 'syria', 'guatemala', 'venezuela', 'armenia',
              'tokelau', 'turkmenistan', 'tuvalu', 'congo', 'azerbaijan', 'bosnia and herzegovina', 'madagascar',
              'bhutan', 'burundi', 'cameroon', 'bangladesh', 'ukraine', 'qatar', 'ethiopia', 'jordan', 'uruguay',
              'brunei', 'papua new guinea', 'haiti', 'fiji', 'united states', 'central african republic', 'senegal',
              'cook islands', 'slovenia', 'suriname', 'iran', 'greece', 'saint helena', 'denmark', 'ghana', 'belgium',
              'albania', 'bahamas', 'lesotho', 'cambodia', 'guernsey', 'kyrgyzstan', 'germany', 'wales', 'samoa',
              'bulgaria', 'finland', 'israel', 'sint maarten', 'malaysia', 'thailand', 'macao', 'estonia', 'guyana',
              'rwanda', 'algeria', 'northern cyprus', 'france', 'pakistan', 'mali', 'belize', 'taiwan',
              'northern ireland', 'croatia', 'indonesia', 'georgia', 'uzbekistan', 'liberia', 'guineabissau',
              'lithuania', 'uganda', 'slovakia', 'equatorial guinea', 'belarus', 'andorra', 'luxembourg', 'malawi',
              'spain', 'oman', 'gambia', 'wallis and futuna', 'honduras', 'jersey', 'congo', 'netherlands', 'latvia',
              'togo', 'montenegro', 'kuwait', 'burkina faso', 'south africa', 'serbia', 'gibraltar', 'guinea',
              'singapore', 'japan', 'nauru', 'cote divoire', 'kiribati', 'isle of man', 'sao tome and principe',
              'comoros', 'malta', 'vanuatu', 'saint vincent and the grenadines', 'united kingdom', 'russia', 'dominica',
              'egypt', 'french polynesia', 'brazil', 'grenada', 'south sudan', 'argentina', 'somalia', 'sri lanka',
              'tanzania', 'kosovo', 'new zealand', 'india', 'bonaire sint eustatius and saba', 'iceland', 'nigeria',
              'seychelles', 'mozambique', 'vietnam', 'hungary', 'niger', 'chad', 'austria', 'greenland', 'kenya',
              'barbados', 'panama', 'saudi arabia', 'yemen', 'djibouti', 'vatican', 'sudan', 'palestine', 'tajikistan',
              'mauritius', 'gabon', 'oceania', 'chile', 'cape verde', 'italy', 'mexico', 'paraguay',
              'antigua and barbuda', 'montserrat', 'cyprus', 'botswana', 'pitcairn', 'laos', 'tunisia', 'switzerland',
              'trinidad and tobago', 'china', 'saint pierre and miquelon', 'north macedonia', 'zimbabwe', 'kazakhstan',
              'morocco', 'faeroe islands', 'namibia', 'norway', 'jamaica', 'scotland', 'eritrea', 'lebanon',
              'bahrain', 'czechia', 'cuba', 'nicaragua', 'monaco', 'peru', 'libya', 'solomon islands', 'romania',
              'san marino', 'nepal', 'falkland islands', 'sweden', 'el salvador', 'england',
              'colombia', 'australia', 'mongolia', 'south korea', 'saint lucia',
              'united arab emirates', 'turkey', 'marshall islands', 'british virgin islands', 'dominican republic',
              'turks and caicos islands', 'new caledonia', 'mauritania', 'bolivia', 'sierra leone', 'costa rica',
              'curacao', 'eswatini', 'saint kitts and nevis', 'cayman islands', 'myanmar', 'zambia'}

    _continents: Set[str] = {"europe", "asia", "european union", "north america", "south america", "africa"}

    _world: Set[str] = {"world"}

    @staticmethod
    def normalize_location_name(location_name: str) -> str:
        def _map_location_abbreviations(string: str) -> str:
            location_name_map: dict = {
                "macedonia": "north macedonia",
                "hk": "hong kong",
                "nz": "new zealand",
                "democratic republic of congo": "congo",
                "uk": "united kingdom",
                "na": "north america",
                "eu": "european union",
                "uae": "united arab emirates",
                "bosnia": "bosnia and herzegovina",
                "salvador": "el salvador",
                "virgin islands": "british virgin islands",
                "us": "united states",
                "usa": "united states",
                "united states of america": "united states"
            }

            return location_name_map[string] if string in location_name_map else string

        location_name = location_name.lower()
        location_name = re.sub(r"\.|-|'|\s*\([^)]+\)", "", location_name)
        location_name = _map_location_abbreviations(location_name)

        return location_name

    @staticmethod
    def add_prepositions_to_location_name(location_name: str) -> str:
        if location_name.lower() == "world":
            return "the world"
        elif location_name.lower() in ["united kingdom", "ukraine", "united states"]:
            return "the " + location_name
        else:
            return location_name

    @staticmethod
    def get_countries() -> Set[str]:
        return Location._countries

    @staticmethod
    def get_continents() -> Set[str]:
        return Location._continents

    @staticmethod
    def get_world() -> Set[str]:
        return Location._world

    @staticmethod
    def get_all() -> Set[str]:
        return Location.get_countries().union(Location.get_continents()).union(Location.get_world())


class LocationRecognizer:
    def recognize_location(self, span: Span) -> Optional[str]:
        location_ents: list = [ent.text for ent in span.ents if ent.label_ == "GPE"]
        if len(location_ents) == 0:
            # If automated entity recognition doesn't work, try a manual approach
            for token in span:
                normalized_token: str = Location.normalize_location_name(token.text)

                if normalized_token in Location.get_all():
                    return normalized_token

            return None
        else:
            return Location.normalize_location_name(location_ents[0])
