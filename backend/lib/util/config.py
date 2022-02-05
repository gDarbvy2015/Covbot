import configparser
import pathlib


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(pathlib.Path(__file__).parent / "config.ini")

    def get_vaccinations_path(self) -> pathlib.Path:
        return pathlib.Path(self.config["FILES"]["vaccinations"])

    def get_cases_path(self) -> pathlib.Path:
        return pathlib.Path(self.config["FILES"]["new_cases"])


if __name__ == '__main__':
    config = Config()
    print(config.get_cases_path())