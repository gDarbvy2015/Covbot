import re


class NLPPipeline:
    def normalize_country_name(self, country_name: str) -> str:
        country_name = country_name.lower()
        country_name = re.sub(r"-|'|\s*\([^)]+\)", "", country_name)
        country_name = self._map_country_abbreviations(country_name)

        return country_name

    def _map_country_abbreviations(self, string: str) -> str:
        # TODO: Extend this
        country_name_map = {
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

        return country_name_map[string] if string in country_name_map else string
