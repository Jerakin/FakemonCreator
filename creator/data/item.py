import json
import copy
from datetime import datetime

import creator.utils.util as util

_NEW_DATA = {
    "Description": ""
}


class Item:
    __initialized = False

    def __init__(self):
        self._name = None
        self.data = None
        self.edited = False

    def __setattr__(self, key, value):
        if self.__initialized:
            self.__dict__["edited"] = True
        super(Item, self).__setattr__(key, value)

    def serialize(self):
        if not self.name:
            now = datetime.now()
            self.name = now.strftime("%m%d%Y%H%M%S")

    def custom(self, data, name):
        self.data = data["items.json"][name]
        self._name = name
        self.__initialized = True

    def load(self, name):
        self.name = name

        data_path = util.DATA / "items.json"
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
        return self.data["Effect"] if "Effect" in self.data else ""

    @description.setter
    def description(self, value):
        self.data["Effect"] = value
