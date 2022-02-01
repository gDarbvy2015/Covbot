class NLPPipeline:
    def normalize_country_name(self, country_name: str) -> str:
        return country_name.lower()