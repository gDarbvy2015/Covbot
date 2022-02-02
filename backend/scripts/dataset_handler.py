import pandas as pd


class DatasetHandler:
    def load_covid_cases(self, path: str) -> pd.DataFrame:
        data = pd.read_csv(path).set_index("date").fillna(0).stack().reset_index()
        data.columns = ["date", "country", "cases"]
        return data

    def load_vaccinations(self, path: str) -> pd.DataFrame:
        pass