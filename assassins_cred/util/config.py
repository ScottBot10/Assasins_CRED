import yaml


class Config:
    def __init__(self, file: str):
        self.file = file

        self.config = None
        with open(file) as f:
            self.config = yaml.safe_load(f)

        self.is_test = self.config["is_test"]

        self.creds = self.config["creds"]
