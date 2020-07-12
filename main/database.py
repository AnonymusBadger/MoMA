import pandas as pd
import os
import re
import time


class Database:
    def __init__(self, path, database=None):
        self._path = path
        self._database = database

    def create_new(self, data):
        save_path = f"{self._path}/data.csv"
        df = pd.DataFrame(data)
        new_order = [
            "Object number",
            "Title",
            "Author",
            "Date",
            "Medium",
            "Dimensions",
            "Artwork URL",
            "Img URL",
        ]
        cols = [col for col in new_order if col in df] + [
            col for col in df if col not in new_order
        ]
        df = df[cols]
        df.to_csv(save_path)
        return

    def find_db(self):
        databases = dict(
            enumerate(
                sorted(
                    filter(
                        None,
                        [
                            " ".join(
                                [
                                    folder.name
                                    for file in os.scandir(folder.path)
                                    if re.match("(.*.csv)", file.name)
                                ]
                            )
                            for folder in os.scandir(self._path)
                            if folder.is_dir()
                        ],
                    )
                ),
                1,
            )
        )
        return databases
