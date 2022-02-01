import pandas as pd


class DatasetHandler:
    def load_covid_cases(self) -> pd.DataFrame:
        path = "../../data/owid/new_cases.csv"
        data = pd.read_csv(path).set_index("date").fillna(0).stack().reset_index()
        data.columns = ["date", "country", "cases"]
        return data

    def load_vaccinations(self, path: str) -> pd.DataFrame:
        pass


if __name__ == '__main__':
    dataset_handler = DatasetHandler()
    new_cases = dataset_handler.load_covid_cases()
    # print(set(new_cases.iloc[:, 1]))