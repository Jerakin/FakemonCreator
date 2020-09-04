import json
import copy
from datetime import datetime

import creator.utils.util as util
import creator.child_views.shared as shared

_NEW_DATA = {
    "Type": "Normal",
    "Move Power": ["None", "None", "None"],
    "Move Time": "",
    "PP": 0,
    "Duration": "",
    "Range": "",
    "Description": ""
  }


class Move:
    __initialized = False

    def __init__(self):
        self._name = None
        self.data = None
        self.edited = False

    def __setattr__(self, key, value):
        if self.__initialized and key != "_Move__initialized":
            self.__dict__["edited"] = True
        super(Move, self).__setattr__(key, value)

    def custom(self, data, name):
        self.data = data["moves.json"][name]
        self._name = name
        self.edited = False
        self.__initialized = True

    def load(self, name):
        self.name = name
        self.data = util.load_move(name)
        self.edited = False
        self.__initialized = True

    def new(self):
        self.data = copy.deepcopy(_NEW_DATA)
        self._name = None
        self.edited = False
        self.__initialized = True

    def _clear(self):
        if "Damage" in self.data:
            for level, d in self.data["Damage"].items():
                if "amount" not in d:
                    del self.data["Damage"]
                    return True
                else:
                    if d["amount"] == "":
                        del self.data["Damage"]
                if "dice_max" not in d:
                    del self.data["Damage"]
                    return True
                else:
                    if d["dice_max"] == "":
                        del self.data["Damage"]
                        return True
        return False

    def serialize(self):
        if not self.name:
            now = datetime.now()
            self.name = now.strftime("%m%d%Y%H%M%S")
        for move in self.data["Move Power"][::-1]:
            if move == "None":
                self.data["Move Power"].remove(move)
        if self._clear():
            shared.show_dialog("Error", f"Move Damage of {self.name} information invalid, skipping saving it.")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def type(self):
        return self.data["Type"]

    @type.setter
    def type(self, value):
        self.data["Type"] = value

    @property
    def move_power1(self):
        return self.data["Move Power"][0] if "Move Power" in self.data and self.data["Move Power"] else None

    @move_power1.setter
    def move_power1(self, value):
        while len(self.data["Move Power"]) < 1:
            self.data["Move Power"].append("None")
        self.data["Move Power"][0] = value

    @property
    def move_power2(self):
        return self.data["Move Power"][1] if "Move Power" in self.data and len(self.data["Move Power"]) == 2 else None

    @move_power2.setter
    def move_power2(self, value):
        while len(self.data["Move Power"]) < 2:
            self.data["Move Power"].append("None")
        self.data["Move Power"][1] = value

    @property
    def move_power3(self):
        return self.data["Move Power"][2] if "Move Power" in self.data and len(self.data["Move Power"]) == 3 else None

    @move_power3.setter
    def move_power3(self, value):
        while len(self.data["Move Power"]) < 3:
            self.data["Move Power"].append("None")
        self.data["Move Power"][2] = value

    @property
    def move_time(self):
        return self.data["Move Time"]

    @move_time.setter
    def move_time(self, value):
        self.data["Move Time"] = value

    @property
    def PP(self):
        return str(self.data["PP"])

    @PP.setter
    def PP(self, value):
        self.data["PP"] = int(value or 0)

    @property
    def casting_time(self):
        return self.data["Move Time"]

    @casting_time.setter
    def casting_time(self, value):
        self.data["Move Time"] = value

    @property
    def duration(self):
        return self.data["Duration"]

    @duration.setter
    def duration(self, value):
        self.data["Duration"] = value

    @property
    def range(self):
        return self.data["Range"]

    @range.setter
    def range(self, value):
        self.data["Range"] = value

    @property
    def description(self):
        return self.data["Description"]

    @description.setter
    def description(self, value):
        self.data["Description"] = value

    @property
    def save(self):
        return self.data["Save"] if "Save" in self.data else None

    @save.setter
    def save(self, value):
        self.data["Save"] = value

    def get_damage_die_property(self, p, level):
        return str(self.data["Damage"][level][p]) if "Damage" in self.data and p in self.data["Damage"][level] else ""

    def set_damage_die_property(self, p, level, amount):
        self.edited = True
        if "Damage" not in self.data:
            self.data["Damage"] = {"1": {}, "5": {}, "10": {}, "17": {}}
            if p in ["move", "level"]:
                amount = bool(amount)
            else:
                amount = int(amount or 0)
        self.data["Damage"][level][p] = amount

    def delete_damage(self):
        if "Damage" in self.data:
            del self.data["Damage"]

    def validate(self):
        util.validate(self.data, util.SCHEMA / "moves.json")
