import pandas as pd

from lib.nlp.nlp_pipeline import NLPPipeline
from lib.util.logger import Logger
from lib.util.config import Config


class DatasetHandler:
    def __init__(self):
        self.nlp_pipeline = NLPPipeline()
        self.logger = Logger(__name__)
        self.config = Config()

    def load_covid_cases(self) -> pd.DataFrame:
        path = self.config.get_cases_path()
        data = pd.read_csv(path).set_index("date").stack().reset_index()
        data.columns = ["date", "country", "cases"]

        data["country_normalized"] = data.apply(lambda row:
                                                self.nlp_pipeline.normalize_country_name(row["country"]), axis=1)

        exclude_countries = ["upper middle income", "summer olympics 2020", "lower middle income",
                             "low income", "international", "world", "high income"]
        data = data[~data["country_normalized"].isin(exclude_countries)]
        return data

    def load_vaccinations(self) -> pd.DataFrame:
        path = self.config.get_vaccinations_path()
        relevant_columns = ["location", "date", "total_vaccinations", "people_vaccinated", "daily_vaccinations",
                            "daily_people_vaccinated"]
        data = pd.read_csv(path)[relevant_columns]
        relevant_columns[0] = "country"
        data.columns = relevant_columns

        data["country_normalized"] = data.apply(lambda row:
                                                self.nlp_pipeline.normalize_country_name(row["country"]), axis=1)

        exclude_countries = ["world", "lower middle income", "low income", "high income", "upper middle income"]
        data = data[~data["country_normalized"].isin(exclude_countries)]
        return data


if __name__ == '__main__':
    dataset_handler = DatasetHandler()
    #new_cases = dataset_handler.load_covid_cases()
    vaccinations = dataset_handler.load_vaccinations()
    print(set(vaccinations["country_normalized"]))