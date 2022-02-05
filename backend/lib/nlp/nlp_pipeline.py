import re


class NLPPipeline:
    def normalize_country_name(self, country_name: str) -> str:
        country_name = country_name.lower()
        country_name = re.sub(r"-|'|\s*\([^)]+\)", "", country_name)

        return country_name
