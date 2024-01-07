import copy

from creator.utils.util import SCHEMA
from creator.utils import validate

_PACKAGE_INDEX_TEMPLATE = {
    "name": "",
    "author": "",
    "description": "",
    "version": 1
}


class Metadata:
    __initialized = False

    def __init__(self):
        self.data = copy.copy(_PACKAGE_INDEX_TEMPLATE)
        self.edited = False

    def __setattr__(self, key, value):
        if self.__initialized and key not in ["edited", "data", "_Metadata__initialized"]:
            self.__dict__["edited"] = True
        super(Metadata, self).__setattr__(key, value)

    def __str__(self):
        return str(self.data)

    def new(self):
        self.data = copy.copy(_PACKAGE_INDEX_TEMPLATE)
        self.__initialized = True

    def load(self, data):
        if data is None:
            data = copy.copy(_PACKAGE_INDEX_TEMPLATE)
        self.data = data
        self.__initialized = True

    @property
    def name(self):
        return self.data["name"]

    @name.setter
    def name(self, value):
        self.data["name"] = value

    @property
    def author(self):
        return self.data["author"]

    @author.setter
    def author(self, value):
        self.data["author"] = value

    @property
    def description(self):
        return self.data["description"]

    @description.setter
    def description(self, value):
        self.data["description"] = value

    @property
    def version(self):
        return str(self.data["version"])

    @version.setter
    def version(self, value):
        self.data["version"] = int(value)

    def validate(self):
        return validate.validate(SCHEMA / "index.json", self.data)
