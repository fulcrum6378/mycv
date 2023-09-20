import os


class FractionalFeatureDB:
    def __init__(self, name: str, key_length: int = 2):
        # ...
        self.data: dict[int, list[str]]

    # ...

    def add_value(self, key: int, sid: str):
        if sid in self.data[key]: raise Exception('This shape ID already exists!')
        # TODO
