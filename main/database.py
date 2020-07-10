import pandas as pd


class Database:
    def __init__(self, path):
        self.path = path

    def create_new(self):
        pd.DataFrame()
