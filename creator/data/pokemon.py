import sys
import json
import copy
from datetime import datetime

import creator.utils.PokemonType.model as PokemonType
import creator.utils.util as util

_NEW_DATA = {
    "Moves": {
      "Level": {},
      "Starting Moves": [
      ],
      "TM": [
      ]
    },
    "index": 0,
    "Abilities": [
    ],
    "Type": [
        "Normal"
    ],
    "SR": 0.125,
    "AC": 0,
    "Hit Dice": 6,
    "HP": 0,
    "WSp": 0,
    "attributes": {
      "STR": 0,
      "DEX": 0,
      "CON": 0,
      "INT": 0,
      "WIS": 0,
      "CHA": 0
    },
    "MIN LVL FD": 1,
    "Skill": [],
    "Res": [],
    "Vul": [
    ],
    "saving_throws": [],
    "Hidden Ability": "Adaptability"
}

_NEW_EXTRA = {
    "flavor": "",
    "height": 1,
    "weight": 1,
    "genus": "Pokémon"
}

_NEW_EVOLVE = {
    "current_stage": 1,
    "total_stages": 1
}


class Pokemon:
    __initialized = False

    def __init__(self):
        self._species = None
        self.data = None
        self.extra = None
        self.evolve = None
        self._legendary = False
        self.edited = False

    def __setattr__(self, key, value):
        if self.__initialized and key not in ["_Pokemon__initialized"]:
            self.__dict__["edited"] = True
        super(Pokemon, self).__setattr__(key, value)

    def serialize(self):
        if not self.species and self.edited:
            now = datetime.now()
            self.species = now.strftime("%m%d%Y%H%M%S")

    def fakemon(self, data, species):
        self.data = data["pokemon.json"][species]
        self.extra = data["pokedex_extra.json"][self.index]
        self.evolve = data["evolve.json"][species]

        self.species = species
        self.edited = False
        self.__initialized = True

    def load(self, species):
        self.species = species

        self.data = util.load_pokemon(species)
        if "saving_throws" not in self.data:
            self.data["saving_throws"] = []

        extra_path = util.DATA / "pokedex_extra.json"
        with extra_path.open("r", encoding="utf-8") as f:
            self.extra = json.load(f)[self.index]

        evolve_path = util.DATA / "evolve.json"
        with evolve_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if species in data:
                self.evolve = data[species]
            else:
                self.evolve = copy.deepcopy(_NEW_EVOLVE)

        self.edited = False
        self.__initialized = True

    def new(self):
        self.data = copy.deepcopy(_NEW_DATA)
        self.extra = copy.deepcopy(_NEW_EXTRA)
        self.evolve = copy.deepcopy(_NEW_EVOLVE)
        self.edited = False
        self.__initialized = True

    @property
    def sprite(self):
        return self.data["sprite"] if "sprite" in self.data else ""

    @sprite.setter
    def sprite(self, value):
        self.data["sprite"] = value

    @property
    def icon(self):
        return self.data["icon"] if "icon" in self.data else ""

    @icon.setter
    def icon(self, value):
        self.data["icon"] = value

    @property
    def species(self):
        return self._species

    @species.setter
    def species(self, value):
        self._species = value

    @property
    def hidden_ability(self):
        return self.data["Hidden Ability"] if "Hidden Ability" in self.data else ""

    @hidden_ability.setter
    def hidden_ability(self, value):
        self.data["Hidden Ability"] = value

    @property
    def save_str(self):
        return "saving_throws" in self.data and "STR" in self.data["saving_throws"]

    @property
    def save_dex(self):
        return "saving_throws" in self.data and "DEX" in self.data["saving_throws"]

    @property
    def save_con(self):
        return "saving_throws" in self.data and "CON" in self.data["saving_throws"]

    @property
    def save_int(self):
        return "saving_throws" in self.data and "INT" in self.data["saving_throws"]

    @property
    def save_wis(self):
        return "saving_throws" in self.data and "WIS" in self.data["saving_throws"]

    @property
    def save_cha(self):
        return "saving_throws" in self.data and "CHA" in self.data["saving_throws"]

    @save_str.setter
    def save_str(self, value):
        if value:
            if "STR" not in self.data["saving_throws"]:
                self.data["saving_throws"].append("STR")
        else:
            self.data["saving_throws"].remove("STR")

    @save_dex.setter
    def save_dex(self, value):
        if value:
            if "DEX" not in self.data["saving_throws"]:
                self.data["saving_throws"].append("DEX")
        else:
            self.data["saving_throws"].remove("DEX")

    @save_con.setter
    def save_con(self, value):
        if value:
            if "CON" not in self.data["saving_throws"]:
                self.data["saving_throws"].append("CON")
        else:
            self.data["saving_throws"].remove("CON")

    @save_int.setter
    def save_int(self, value):
        if value:
            if "INT" not in self.data["saving_throws"]:
                self.data["saving_throws"].append("INT")
        else:
            self.data["saving_throws"].remove("INT")

    @save_wis.setter
    def save_wis(self, value):
        if value:
            if "WIS" not in self.data["saving_throws"]:
                self.data["saving_throws"].append("WIS")
        else:
            self.data["saving_throws"].remove("WIS")

    @save_cha.setter
    def save_cha(self, value):
        if value:
            if "CHA" not in self.data["saving_throws"]:
                self.data["saving_throws"].append("CHA")
        else:
            self.data["saving_throws"].remove("CHA")


    @property
    def saving_throw2(self):
        if "saving_throws" in self.data:
            st = self.data["saving_throws"]
            return st[1] if len(st) == 2 else None

    @saving_throw2.setter
    def saving_throw2(self, value):
        if "saving_throws" not in self.data:
            self.data["saving_throws"] = ["None", value]
        else:
            if len(self.data["saving_throws"]) == 1:
                self.data["saving_throws"].append(value)
            elif len(self.data["saving_throws"]) == 0:
                self.data["saving_throws"].append("None")
                self.data["saving_throws"].append(value)
            else:
                self.data["saving_throws"][1] = value

    @property
    def saving_throw1(self):
        if "saving_throws" in self.data and self.data["saving_throws"]:
            return self.data["saving_throws"][0]
        return "None"

    @saving_throw1.setter
    def saving_throw1(self, value):
        if "saving_throws" not in self.data:
            self.data["saving_throws"] = ["None"]
        self.data["saving_throws"][0] = value

    def update_type_res(self):
        for t in ["Imm", "Res", "Vul"]:
            if t in self.data:
                self.data[t] = []
        for imm in self.immunities:
            self.set_res("Imm", imm)
        for res in self.resistances:
            self.set_res("Res", res)
        for vul in self.vulnerabilities:
            self.set_res("Vul", vul)

    @property
    def type1(self):
        return self.data["Type"][0] if "Type" in self.data and self.data["Type"] else None

    @type1.setter
    def type1(self, value):
        if self.data["Type"]:
            self.data["Type"][0] = value
        else:
            self.data["Type"] = [value]
        self.update_type_res()

    @property
    def type2(self):
        return self.data["Type"][1] if "Type" in self.data and len(self.data["Type"]) > 1 else None

    @type2.setter
    def type2(self, value):
        if len(self.data["Type"]) == 1 and value != "None":
            self.data["Type"].append(value)
        else:
            if value == "None":
                del self.data["Type"][1]
            else:
                self.data["Type"][1] = value
        self.update_type_res()

    @property
    def sr(self):
        return str(self.data["SR"]) if self.data["SR"] < 1 else str(int(self.data["SR"]))

    @sr.setter
    def sr(self, value):
        self.data["SR"] = float(value)

    @property
    def hit_points(self):
        return str(self.data["HP"])

    @hit_points.setter
    def hit_points(self, value):
        self.data["HP"] = int(value if value else 0)

    @property
    def hit_dice(self):
        return str(self.data["Hit Dice"])

    @hit_dice.setter
    def hit_dice(self, value):
        self.data["Hit Dice"] = int(value if value else 0)

    @property
    def armor_class(self):
        return str(self.data["AC"])

    @armor_class.setter
    def armor_class(self, value):
        self.data["AC"] = int(value if value else 0)

    @property
    def level(self):
        return str(self.data["MIN LVL FD"])

    @level.setter
    def level(self, value):
        self.data["MIN LVL FD"] = int(value if value else 0)

    @property
    def index(self):
        return str(self.data["index"])

    @index.setter
    def index(self, value):
        self.data["index"] = int(value if value else 0)

    def set_res(self, t, value):
        if t in self.data:
            if value not in self.data[t]:
                self.data[t].append(value)
        else:
            self.data[t] = [value]

    @property
    def vulnerabilities(self):
        return PokemonType.SingleModel(self.type1, self.type2).vulnerabilities

    @property
    def immunities(self):
        return PokemonType.SingleModel(self.type1, self.type2).immunities

    @property
    def resistances(self):
        return PokemonType.SingleModel(self.type1, self.type2).resistances

    def add_move(self, t, move):
        if t in self.data["Moves"]["Level"]:
            if move not in self.data["Moves"]["Level"][t]:
                self.data["Moves"]["Level"][t].append(move)
        else:
            self.data["Moves"]["Level"][t] = [move]

    def get_level_moves(self, t):
        return self.data["Moves"]["Level"][t] if t in self.data["Moves"]["Level"] else []

    def remove_level_move(self, t, move):
        self.edited = True
        self.data["Moves"]["Level"][t].remove(move)

    def remove_move(self, t, move):
        self.edited = True
        self.data["Moves"][t].remove(move)

    def remove_entry(self, t, entry):
        self.edited = True
        self.data[t].remove(entry)

    @property
    def evolve_with_move(self):
        return str(self.evolve["move"]) if "move" in self.evolve else ""

    @evolve_with_move.setter
    def evolve_with_move(self, value):
        if value == "" and "move" in self.evolve:
            del self.evolve["move"]
        else:
            self.evolve["move"] = value

    @property
    def moves_level2(self):
        return self.get_level_moves("2")

    @moves_level2.setter
    def moves_level2(self, value):
        self.add_move("2", value)

    @property
    def moves_level6(self):
        return self.get_level_moves("6")

    @moves_level6.setter
    def moves_level6(self, value):
        self.add_move("6", value)

    @property
    def moves_level10(self):
        return self.get_level_moves("10")

    @moves_level10.setter
    def moves_level10(self, value):
        self.add_move("10", value)

    @property
    def moves_level14(self):
        return self.get_level_moves("14")

    @moves_level14.setter
    def moves_level14(self, value):
        self.add_move("14", value)

    @property
    def moves_level18(self):
        return self.get_level_moves("18")

    @moves_level18.setter
    def moves_level18(self, value):
        self.add_move("18", value)

    @property
    def moves_starting(self):
        return self.data["Moves"]["Starting Moves"]

    @moves_starting.setter
    def moves_starting(self, value):
        if value not in self.data["Moves"]["Starting Moves"]:
            self.data["Moves"]["Starting Moves"].append(value)

    @property
    def moves_tm(self):
        return [str(x) for x in self.data["Moves"]["TM"]] if "TM" in self.data["Moves"] else []

    @moves_tm.setter
    def moves_tm(self, value):
        value = int(value.split(" ")[0])
        if "TM" not in self.data["Moves"]:
            self.data["Moves"]["TM"] = []
        if value not in self.data["Moves"]["TM"]:
            self.data["Moves"]["TM"].append(int(value if value else 0))

    @property
    def abilities(self):
        return self.data["Abilities"]

    @abilities.setter
    def abilities(self, value):
        if "Abilities" not in self.data:
            self.data["Abilities"] = []
        if value not in self.data["Abilities"]:
            self.data["Abilities"].append(value)

    @property
    def skills(self):
        return self.data["Skill"] if "Skill" in self.data else []

    @skills.setter
    def skills(self, value):
        if "Skill" not in self.data:
            self.data["Skill"] = []
        if value not in self.data["Skill"]:
            self.data["Skill"].append(value)

    def remove_evolution(self, evolution):
        self.evolve["into"].remove(evolution)

    @property
    def evolve_into(self):
        return self.evolve["into"] if "into" in self.evolve else []

    @evolve_into.setter
    def evolve_into(self, value):
        if "into" in self.evolve:
            if value not in self.evolve["into"]:
                self.evolve["into"].append(value)
        else:
            self.evolve["into"] = [value]

    @property
    def evolve_level(self):
        return str(self.evolve["level"]) if "level" in self.evolve else ""

    @evolve_level.setter
    def evolve_level(self, value):
        self.evolve["level"] = int(value if value else 0)

    @property
    def evolve_points(self):
        return str(self.evolve["points"]) if "points" in self.evolve else ""

    @evolve_points.setter
    def evolve_points(self, value):
        self.evolve["points"] = int(value if value else 0)

    @property
    def evolve_total_stages(self):
        return str(self.evolve["total_stages"])

    @evolve_total_stages.setter
    def evolve_total_stages(self, value):
        self.evolve["total_stages"] = int(value if value else 0)

    @property
    def evolve_current_stages(self):
        return str(self.evolve["current_stage"])

    @evolve_current_stages.setter
    def evolve_current_stages(self, value):
        self.evolve["current_stage"] = int(value if value else 0)

    @property
    def walking(self):
        return str(self.data["WSp"]) if "WSp" in self.data else ""

    @walking.setter
    def walking(self, value):
        self.data["WSp"] = int(value if value else 0)

    @property
    def swimming(self):
        return str(self.data["SSp"]) if "SSp" in self.data else ""

    @swimming.setter
    def swimming(self, value):
        self.data["SSp"] = int(value if value else 0)

    @property
    def climbing(self):
        return str(self.data["Climbing Speed"]) if "Climbing Speed" in self.data else ""

    @climbing.setter
    def climbing(self, value):
        self.data["Climbing Speed"] = int(value if value else 0)

    @property
    def flying(self):
        return str(self.data["Fsp"]) if "Fsp" in self.data else ""

    @flying.setter
    def flying(self, value):
        self.data["Fsp"] = int(value if value else 0)

    def set_sense(self, sense, value):
        if "Senses" not in self.data:
            self.data["Senses"] = []
        for s in self.data["Senses"][::-1]:
            if s.startswith(sense):
                self.data["Senses"].remove(s)
        self.data["Senses"].append("{} {}ft.".format(sense, value))

    def get_sense(self, sense):
        if "Senses" in self.data:
            for s in self.data["Senses"]:
                if sense in s:
                    digits = [n for n in s if n.isdigit()]
                    return ''.join(digits)
        return ""

    @property
    def darkvision(self):
        return self.get_sense("Darkvision")

    @darkvision.setter
    def darkvision(self, value):
        self.set_sense("Darkvision", value)

    @property
    def tremorsense(self):
        return self.get_sense("Tremorsense")

    @tremorsense.setter
    def tremorsense(self, value):
        self.set_sense("Tremorsense", value)

    @property
    def blindsight(self):
        return self.get_sense("Blindsight")

    @blindsight.setter
    def blindsight(self, value):
        self.set_sense("Blindsight", value)

    @property
    def truesight(self):
        return self.get_sense("Truesight")

    @truesight.setter
    def truesight(self, value):
        self.set_sense("Truesight", value)

    @property
    def weight(self):
        return str(self.extra["weight"])

    @weight.setter
    def weight(self, value):
        value = value.replace(",", ".")
        self.extra["weight"] = float(value if value else 0)

    @property
    def height(self):
        return str(self.extra["height"])

    @height.setter
    def height(self, value):
        value = value.replace(",", ".")

        self.extra["height"] = float(value if value else 0)

    @property
    def genus(self):
        return self.extra["genus"]

    @genus.setter
    def genus(self, value):
        self.extra["genus"] = value

    @property
    def flavor(self):
        return self.extra["flavor"]

    @flavor.setter
    def flavor(self, value):
        self.extra["flavor"] = value

    def set_attributes(self, attribute, value):
        self.data["attributes"][attribute] = int(value if value else 0)

    def get_attribute(self, attribute):
        return str(self.data["attributes"][attribute])

    @property
    def STR(self):
        return self.get_attribute("STR")

    @STR.setter
    def STR(self, value):
        self.set_attributes("STR", value)

    @property
    def DEX(self):
        return self.get_attribute("DEX")

    @DEX.setter
    def DEX(self, value):
        self.set_attributes("DEX", value)

    @property
    def CON(self):
        return self.get_attribute("CON")

    @CON.setter
    def CON(self, value):
        self.set_attributes("CON", value)

    @property
    def WIS(self):
        return self.get_attribute("WIS")

    @WIS.setter
    def WIS(self, value):
        self.set_attributes("WIS", value)

    @property
    def INT(self):
        return self.get_attribute("INT")

    @INT.setter
    def INT(self, value):
        self.set_attributes("INT", value)

    @property
    def CHA(self):
        return self.get_attribute("CHA")

    @CHA.setter
    def CHA(self, value):
        self.set_attributes("CHA", value)



