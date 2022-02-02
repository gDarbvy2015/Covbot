import pandas as pd

from lib.nlp.nlp_pipeline import NLPPipeline


class DatasetHandler:
    def __init__(self):
        self.nlp_pipeline = NLPPipeline()

    def load_covid_cases(self) -> pd.DataFrame:
        path = "../../data/owid/new_cases.csv"
        data = pd.read_csv(path).set_index("date").fillna(0).stack().reset_index()
        data.columns = ["date", "country", "cases"]

        data["country_normalized"] = data.apply(lambda row:
                                                self.nlp_pipeline.normalize_country_name(row["country"]), axis=1)

        exclude_countries = ["upper middle income", "summer olympics 2020", "lower middle income",
                             "low income", "international", "world"]
        data = data[~data["country_normalized"].isin(exclude_countries)]
        return data

    def load_vaccinations(self, path: str) -> pd.DataFrame:
        pass


if __name__ == '__main__':
    dataset_handler = DatasetHandler()
    new_cases = dataset_handler.load_covid_cases()
    print(set(new_cases["country_normalized"]))