import os
from datetime import datetime, timedelta
from typing import List

import pandas as pd
from pandas import DataFrame

from lib.nlp.nlp_processor import NLPProcessor
from lib.util.logger import Logger


class DatasetHandler:
    def __init__(self):
        self.nlp_pipeline: NLPProcessor = NLPProcessor()
        self.logger: Logger = Logger(__name__)

    def load_covid_cases(self) -> DataFrame:
        path: str = os.environ.get("COVBOT_CASES_PATH")
        data: DataFrame = pd.read_csv(path).set_index("date").stack().reset_index()
        data.columns = ["date", "country", "cases"]

        data["country_normalized"] = data.apply(lambda row:
                                                self.nlp_pipeline.normalize_country_name(row["country"]), axis=1)


        exclude_countries = ["upper middle income", "summer olympics 2020", "lower middle income",
                             "low income", "international", "world", "high income", "europe", "asia",
                             "european union", "north america"]
        data = data[~data["country_normalized"].isin(exclude_countries)]
        data = self._add_cumulative_cases(data)

        data["id"] = data.index + 1
        return data

    def load_vaccinations(self) -> pd.DataFrame:
        path: str = os.environ.get("COVBOT_VACCINATIONS_PATH")
        relevant_columns: List[str] = ["location", "date", "total_vaccinations", "people_vaccinated",
                                       "daily_vaccinations",
                                       "daily_people_vaccinated"]
        data = pd.read_csv(path)[relevant_columns]
        relevant_columns[0] = "country"
        data.columns = relevant_columns

        data["country_normalized"] = data.apply(lambda row:
                                                self.nlp_pipeline.normalize_country_name(row["country"]), axis=1)

        exclude_countries: List[str] = ["world", "lower middle income", "low income", "high income",
                                        "upper middle income", "europe", "asia", "european union",
                                        "north america"]
        data = data[~data["country_normalized"].isin(exclude_countries)]
        data = self._add_cumulative_vaccinations(data)

        data["id"] = data.index + 1
        return data

    def _increase_date_by_one(self, date: str) -> str:
        date_format: str = "%Y-%m-%d"
        date_obj: datetime.date = datetime.strptime(date, date_format).date()
        date_obj += timedelta(days=1)
        return date_obj.strftime(date_format)

    def _add_cumulative_cases(self, df: DataFrame) -> DataFrame:
        df["date_in_seconds"] = df.apply(lambda row: datetime.strptime(row["date"], "%Y-%m-%d").timestamp(), axis=1)
        df = df.set_index(["country", "date_in_seconds"]).sort_index()
        df["cumulative_cases"] = df["cases"].fillna(0).groupby("country").cumsum()
        return df.reset_index().drop("date_in_seconds", axis=1)

    def _add_cumulative_vaccinations(self, df: DataFrame) -> DataFrame:
        df["date_in_seconds"] = df.apply(lambda row: datetime.strptime(row["date"], "%Y-%m-%d").timestamp(), axis=1)
        df = df.set_index(["country", "date_in_seconds"]).sort_index()
        df["total_vaccinations"] = df["daily_vaccinations"].fillna(0).groupby("country").cumsum()
        df["people_vaccinated"] = df["daily_people_vaccinated"].fillna(0).groupby("country").cumsum()
        return df.reset_index().drop("date_in_seconds", axis=1)


if __name__ == '__main__':
    dataset_handler = DatasetHandler()
    vaccinations = dataset_handler.load_vaccinations()
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    print(vaccinations[vaccinations["country"] == "China"])
