# model.py
# Maximillian Tinati
# December 15, 2013
"""This module contains the model for the Pokemon type calculation app."""
from creator.utils.PokemonType.thetypes import *

# Useful constant: list containing all pokemon types as separate strings in lowercase.
TYPE_LIST = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting',
             'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost',
             'dragon', 'dark', 'steel', 'fairy']

TYPE_ATTACKS = ['normalAtk', 'fireAtk', 'waterAtk', 'electricAtk', 'grassAtk',
                'iceAtk', 'fightingAtk', 'poisonAtk', 'groundAtk', 'flyingAtk',
                'psychicAtk', 'bugAtk', 'rockAtk', 'ghostAtk', 'dragonAtk',
                'darkAtk', 'steelAtk', 'fairyAtk']


TYPE_MAP = {'normalAtk': 'Normal',
            'fireAtk': 'Fire',
            'waterAtk': 'Water',
            'electricAtk': 'Electric',
            'grassAtk': 'Grass',
            'iceAtk': 'Ice',
            'fightingAtk': 'Fighting',
            'poisonAtk': 'Poison',
            'groundAtk': 'Ground',
            'flyingAtk': 'Flying',
            'psychicAtk': 'Psychic',
            'bugAtk': 'Bug',
            'rockAtk': 'Rock',
            'ghostAtk': 'Ghost',
            'dragonAtk': 'Dragon',
            'darkAtk': 'Dark',
            'steelAtk': 'Steel',
            'fairyAtk': 'Fairy'
            }

def valid_type(thetype):
    """Returns: True if <thetype> is a string representing a valid Pokemon type;
    False otherwise."""
    assert isinstance(thetype, str)
    
    thetype = thetype.lower()   # default string to a standard case for easy checking
    assert thetype in TYPE_LIST


def typeChecker(thetype):
        """Returns: a <Type> object corresponding to the specified Pokemon type
        <thetype>.
        
        Precondition:  <thetype> is a str and a valid Pokemon type."""
        assert isinstance(thetype, str)
        
        thetype = thetype.lower()
        
        if thetype == 'normal':
            return Normal()
        elif thetype == 'fire':
            return Fire()
        elif thetype == 'water':
            return Water()
        elif thetype == 'electric':
            return Electric()
        elif thetype == 'grass':
            return Grass()
        elif thetype == 'ice':
            return Ice()
        elif thetype == 'fighting':
            return Fighting()
        elif thetype == 'poison':
            return Poison()
        elif thetype == 'ground':
            return Ground()
        elif thetype == 'flying':
            return Flying()
        elif thetype == 'psychic':
            return Psychic()
        elif thetype == 'bug':
            return Bug()
        elif thetype == 'rock':
            return Rock()
        elif thetype == 'ghost':
            return Ghost()
        elif thetype == 'dragon':
            return Dragon()
        elif thetype == 'dark':
            return Dark()
        elif thetype == 'steel':
            return Steel()
        elif thetype == 'fairy':
            return Fairy()


class SingleModel(object):
    """An instance of this class models incoming attack effectiveness against
    A SINGLE defending pokemon, whose type(s) are chosen upon class construction.
    This model calls the appropriate single type classes from thetypes.py, and
    determines the overall effectiveness if the defending pokemon is dual-typed.
    
    Instance attributes:
        types:      a list containing the types of the pokemon to be analyzed
                    [list of 1-2 <Type> objects if any are selected, None otherwise]
        sumType:    a fictional pokemon type containing the effectiveness of
                    incoming attacks to both of the Pokemon's types
                    [a single <Type> object if types specified, None otherwise]"""
    
    def __init__(self, type1=None, type2=None):
        """Initializer: constructs an object of type <SingleModel> with all initial
        variable states corresponding to  the inputted Pokemon types.
        
        Precondition: type1 and type2 are strings and valid Pokemon types."""
        # assert valid_type(type1)
        # assert valid_type(type2)
        
        # Create appropriate Type classes if any and append to <types>
        self.types = []
        self.sum_of_type = None

        if type1 is not None:
            type_obj1 = typeChecker(type1)
            self.types.append(type_obj1)
        if type2 is not None:
            type_obj2 = typeChecker(type2)
            self.types.append(type_obj2)
        
        # Initialize sumType att using helper method b/c really long
        self.construct_sum_type()

    @property
    def vulnerabilities(self):
        return [TYPE_MAP[attr] for attr in dir(self.sum_of_type) if
                not callable(getattr(self.sum_of_type, attr)) and not attr.startswith("__") and getattr(
                    self.sum_of_type, attr) > 1]

    @property
    def immunities(self):
        return [TYPE_MAP[attr] for attr in dir(self.sum_of_type) if
                not callable(getattr(self.sum_of_type, attr)) and not attr.startswith("__") and getattr(
                    self.sum_of_type, attr) == 0]

    @property
    def resistances(self):
        return [TYPE_MAP[attr] for attr in dir(self.sum_of_type) if
                not callable(getattr(self.sum_of_type, attr)) and not attr.startswith("__") and getattr(
                    self.sum_of_type, attr) < 1]

    def construct_sum_type(self):
        """Method to handle initialization of the <sumType> attribute.
        Initially, <sumType> is None.  If <types> contains only a single type,
        then <sumType> will contain that particular Type obj.  If <types>
        contains 2 Type objs, then a dual-type Type obj is constructed and stored
        in <sumType>."""
        # Default to None
        self.sum_of_type = None
        
        # If 1 type specified, set the sumType to this type
        if len(self.types) == 1:
            self.sum_of_type = self.types[0]
        
        # If 2 types specified, construct artificial Type w/multiplied effectivenesses
        elif len(self.types) == 2:
            type1 = self.types[0]
            type2 = self.types[1]
            self.sum_of_type = Type()
            
            self.sum_of_type.normalAtk = type1.normalAtk * type2.normalAtk
            self.sum_of_type.fireAtk = type1.fireAtk * type2.fireAtk
            self.sum_of_type.waterAtk = type1.waterAtk * type2.waterAtk
            self.sum_of_type.electricAtk = type1.electricAtk * type2.electricAtk
            self.sum_of_type.grassAtk = type1.grassAtk * type2.grassAtk
            self.sum_of_type.iceAtk = type1.iceAtk * type2.iceAtk
            self.sum_of_type.fightingAtk = type1.fightingAtk * type2.fightingAtk
            self.sum_of_type.poisonAtk = type1.poisonAtk * type2.poisonAtk
            self.sum_of_type.groundAtk = type1.groundAtk * type2.groundAtk
            self.sum_of_type.flyingAtk = type1.flyingAtk * type2.flyingAtk
            self.sum_of_type.psychicAtk = type1.psychicAtk * type2.psychicAtk
            self.sum_of_type.bugAtk = type1.bugAtk * type2.bugAtk
            self.sum_of_type.rockAtk = type1.rockAtk * type2.rockAtk
            self.sum_of_type.ghostAtk = type1.ghostAtk * type2.ghostAtk
            self.sum_of_type.dragonAtk = type1.dragonAtk * type2.dragonAtk
            self.sum_of_type.darkAtk = type1.darkAtk * type2.darkAtk
            self.sum_of_type.steelAtk = type1.steelAtk * type2.steelAtk
            self.sum_of_type.fairyAtk = type1.fairyAtk * type2.fairyAtk
