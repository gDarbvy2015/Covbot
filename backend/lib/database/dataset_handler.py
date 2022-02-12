from datetime import datetime, timedelta

import pandas
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
        data = self._add_cumulative_cases(data)
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

    def _increase_date_by_one(self, date: str) -> str:
        date_format = "%Y-%m-%d"
        date_obj = datetime.strptime(date, date_format).date()
        date_obj += timedelta(days=1)
        return date_obj.strftime(date_format)

    def _add_cumulative_cases(self, df: pandas.DataFrame) -> pandas.DataFrame:
        df["date_in_seconds"] = df.apply(lambda row:
                                                       datetime.strptime(row["date"], "%Y-%m-%d").timestamp(), axis=1)
        df = df.set_index(["country", "date_in_seconds"]).sort_index()
        df["cumulative_cases"] = df["cases"].groupby("country").cumsum()
        return df.reset_index().drop("date_in_seconds", axis=1)


if __name__ == '__main__':
    dataset_handler = DatasetHandler()