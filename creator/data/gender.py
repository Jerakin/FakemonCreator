import json

import creator.utils.util as util


class Gender:
    __initialized = False

    def __init__(self):
        self._species = None
        self.data = None
        self.edited = False

    def __setattr__(self, key, value):
        if self.__initialized:
            self.__dict__["edited"] = True
        super(Gender, self).__setattr__(key, value)

    def load(self, name):
        data_path = util.DATA / "gender.json"
        with data_path.open("r", encoding="utf-8") as f:
            self.data = json.load(f)[name]
        self.__initialized = True

    def new(self):
        self.data = {}
        self.edited = False
        self.__initialized = True

    def serialize(self):
        pass

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, species):
        self._species = species

    @property
    def gender(self):
        return self.data[self.species]

    @gender.setter
    def gender(self, gender):
        self.data[self.species] = gender
