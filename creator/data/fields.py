from enum import Enum


SR = [str(0.125), str(0.25), str(0.5)]
for i in range(15):
    SR.append(str(i+1))

SKILLS = [
    "",
    "Athletics",
    "Acrobatics",
    "Sleight of Hand",
    "Stealth",
    "Arcana",
    "History",
    "Investigation",
    "Nature",
    "Religion",
    "Animal Handling",
    "Insight",
    "Medicine",
    "Perception",
    "Survival",
    "Deception",
    "Intimidation",
    "Performance",
    "Persuasion"
]

SENSES = [
    "",
    "Darkvision",
    "Tremorsense",
    "Truesight",
    "Blindsight"
]


class Type(str, Enum):
    NORMAL = "Normal"
    FIGHTING = "Fighting"
    FLYING = "Flying"
    POISON = "Poison"
    GROUND = "Ground"
    ROCK = "Rock"
    BUG = "Bug"
    GHOST = "Ghost"
    STEEL = "Steel"
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    ELECTRIC = "Electric"
    PSYCHIC = "Psychic"
    ICE = "Ice"
    DRAGON = "Dragon"
    DARK = "Dark"
    FAIRY = "Fairy"


class Attributes(str, Enum):
    STRENGTH = "STR"
    DEXTERITY = "DEX"
    CONSTITUTION = "CON"
    INTELLIGENCE = "INT"
    WISDOM = "WIS"
    CHARISMA = "CHA"


class Dice(str, Enum):
    FOUR = "4"
    SIX = "6"
    EIGHT = "8"
    TEN = "10"
    TWELVE = "12"
    TWENTY = "20"