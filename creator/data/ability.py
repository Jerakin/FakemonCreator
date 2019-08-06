from pathlib import Path
import json
import copy
import sys
from datetime import datetime

_NEW_DATA = {
    "Description": ""
}

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)


class Ability:
    __initialized = False

    def __init__(self):
        self._name = None
        self.data = None
        self.edited = False

    def __setattr__(self, key, value):
        if self.__initialized:
            self.__dict__["edited"] = True
        super(Ability, self).__setattr__(key, value)

    def serialize(self):
        if not self.name:
            now = datetime.now()
            self.name = now.strftime("%m%d%Y%H%M%S")

    def custom(self, data, name):
        self.data = data["abilities.json"][name]
        self._name = name
        self.__initialized = True

    def load(self, name):
        self.name = name

        data_path = Path(root / "res/data/abilities.json")
        with data_path.open("r", encoding="utf-8") as f:
            self.data = json.load(f)[name]
        self.__initialized = True

    def new(self):
        self.data = copy.deepcopy(_NEW_DATA)
        self._name = None
        self.edited = False
        self.__initialized = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self.data["Description"]

    @description.setter
    def description(self, value):
        self.data["Description"] = value
