# types.py
# Maximillian Tinati
# December 14, 2013
"""Module contains type classes for all 18 Pokemon types.  Instances of a type
contain 18 attributes corresponding to its weakness to attacks of all types."""


class Type(object):
    """Parent class for Pokemon types.  An instance represents a standard
    Pokemon typing, with all of its strengths and weaknesses.  Note: this is
    a parent class for all 18 different type subclasses, and as such all of
    these instance attributes will be defaulted to 1.0
    
    Instance attributes:
        normalAtk:   effectiveness of incoming normal attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        fireAtk:     effectiveness of incoming fire attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        waterAtk:    effectiveness of incoming water attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        electricAtk: effectiveness of incoming electric attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        grassAtk:    effectiveness of incoming grass attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        iceAtk:      effectiveness of incoming ice attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        fightingAtk: effectiveness of incoming fighting attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        poisonAtk:   effectiveness of incoming poison attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        groundAtk:   effectiveness of incoming ground attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        flyingAtk:   effectiveness of incoming flying attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        psychicAtk:  effectiveness of incoming psychic attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        bugAtk:      effectiveness of incoming bug attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        rockAtk:     effectiveness of incoming rock attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        ghostAtk:    effectiveness of incoming ghost attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        dragonAtk    effectiveness of incoming dragon attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        darkAtk:     effectiveness of incoming dark attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        steelAtk:    effectiveness of incoming steel attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]
        fairyAtk:    effectiveness of incoming fairy attack
                     [float of value 0.0, 0.25, 0.5, 1.0, 2.0, or 4.0]"""
    
    def __init__(self):
        """Initializer: constructs an object of type <Type> and defaults all
        attributes to 1.0 effectiveness."""
        self.normalAtk = 1.0
        self.fireAtk = 1.0
        self.waterAtk = 1.0
        self.electricAtk = 1.0
        self.grassAtk = 1.0
        self.iceAtk = 1.0
        self.fightingAtk = 1.0
        self.poisonAtk = 1.0
        self.groundAtk = 1.0
        self.flyingAtk = 1.0
        self.psychicAtk = 1.0
        self.bugAtk = 1.0
        self.rockAtk = 1.0
        self.ghostAtk = 1.0
        self.dragonAtk = 1.0
        self.darkAtk = 1.0
        self.steelAtk = 1.0
        self.fairyAtk = 1.0


class Normal(Type):
    """Subclass of type <Type> representing the Normal type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fightingAtk = 2.0
        self.ghostAtk = 0.0


class Fire(Type):
    """Subclass of type <Type> representing the Fire type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fireAtk = 0.5
        self.waterAtk = 2.0
        self.grassAtk = 0.5
        self.iceAtk = 0.5
        self.groundAtk = 2.0
        self.bugAtk = 0.5
        self.rockAtk = 2.0
        self.steelAtk = 0.5
        self.fairyAtk = 0.5


class Water(Type):
    """Subclass of type <Type> representing the Water type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fireAtk = 0.5
        self.waterAtk = 0.5
        self.electricAtk = 2.0
        self.grassAtk = 2.0
        self.iceAtk = 0.5
        self.steelAtk = 0.5


class Electric(Type):
    """Subclass of type <Type> representing the Electric type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.electricAtk = 0.5
        self.groundAtk = 2.0
        self.flyingAtk = 0.5
        self.steelAtk = 0.5


class Grass(Type):
    """Subclass of type <Type> representing the Grass type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fireAtk = 2.0
        self.waterAtk = 0.5
        self.electricAtk = 0.5
        self.grassAtk = 0.5
        self.iceAtk = 2.0
        self.poisonAtk = 2.0
        self.groundAtk = 0.5
        self.flyingAtk = 2.0
        self.bugAtk = 2.0


class Ice(Type):
    """Subclass of type <Type> representing the Ice type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fireAtk = 2.0
        self.iceAtk = 0.5
        self.fightingAtk = 2.0
        self.rockAtk = 2.0
        self.steelAtk = 2.0


class Fighting(Type):
    """Subclass of type <Type> representing the Fighting type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.flyingAtk = 2.0
        self.psychicAtk = 2.0
        self.bugAtk = 0.5
        self.rockAtk = 0.5
        self.darkAtk = 0.5
        self.fairyAtk = 2.0


class Poison(Type):
    """Subclass of type <Type> representing the Poison type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.grassAtk = 0.5
        self.fightingAtk = 0.5
        self.poisonAtk = 0.5
        self.groundAtk = 2.0
        self.psychicAtk = 2.0
        self.bugAtk = 0.5
        self.fairyAtk = 0.5


class Ground(Type):
    """Subclass of type <Type> representing the Ground type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.waterAtk = 2.0
        self.electricAtk = 0.0
        self.grassAtk = 2.0
        self.iceAtk = 2.0
        self.poisonAtk = 0.5
        self.rockAtk = 0.5


class Flying(Type):
    """Subclass of type <Type> representing the Flying type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.electricAtk = 2.0
        self.grassAtk = 0.5
        self.iceAtk = 2.0
        self.fightingAtk = 0.5
        self.groundAtk = 0.0
        self.bugAtk = 0.5
        self.rockAtk = 2.0


class Psychic(Type):
    """Subclass of type <Type> representing the Psychic type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fightingAtk = 0.5
        self.psychicAtk = 0.5
        self.bugAtk = 2.0
        self.ghostAtk = 2.0
        self.darkAtk = 2.0


class Bug(Type):
    """Subclass of type <Type> representing the Bug type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fireAtk = 2.0
        self.grassAtk = 0.5
        self.fightingAtk = 0.5
        self.groundAtk = 0.5
        self.flyingAtk = 2.0
        self.rockAtk = 2.0


class Rock(Type):
    """Subclass of type <Type> representing the Rock type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.normalAtk = 0.5
        self.fireAtk = 0.5
        self.waterAtk = 2.0
        self.grassAtk = 2.0
        self.fightingAtk = 2.0
        self.poisonAtk = 0.5
        self.groundAtk = 2.0
        self.flyingAtk = 0.5
        self.steelAtk = 2.0


class Ghost(Type):
    """Subclass of type <Type> representing the Ghost type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.normalAtk = 0.0
        self.fightingAtk = 0.0
        self.poisonAtk = 0.5
        self.bugAtk = 0.5
        self.ghostAtk = 2.0
        self.darkAtk = 2.0


class Dragon(Type):
    """Subclass of type <Type> representing the Dragon type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fireAtk = 0.5
        self.waterAtk = 0.5
        self.electricAtk = 0.5
        self.grassAtk = 0.5
        self.iceAtk = 2.0
        self.dragonAtk = 2.0
        self.fairyAtk = 2.0


class Dark(Type):
    """Subclass of type <Type> representing the Dark type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fightingAtk = 2.0
        self.psychicAtk = 0.0
        self.bugAtk = 2.0
        self.ghostAtk = 0.5
        self.darkAtk = 0.5
        self.fairyAtk = 2.0


class Steel(Type):
    """Subclass of type <Type> representing the Steel type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.normalAtk = 0.5
        self.fireAtk = 2.0
        self.grassAtk = 0.5
        self.iceAtk = 0.5
        self.fightAtk = 2.0
        self.poisonAtk = 0.0
        self.groundAtk = 2.0
        self.flyingAtk = 0.5
        self.psychicAtk = 0.5
        self.bugAtk = 0.5
        self.rockAtk = 0.5
        self.dragonAtk = 0.5
        self.steelAtk = 0.5
        self.fairyAtk = 0.5


class Fairy(Type):
    """Subclass of type <Type> representing the Fairy type in Pokemon. All
    instance attributes inherited from <Type> with the addition of no others.
    Attributes are modified to reflect the effectiveness of this particular
    type."""
    
    def __init__(self):
        """Initializer: uses the generic parent class' initializer and then
        modifies the attributes to reflect this type's str's and weaknesses."""
        Type.__init__(self)
        self.fightingAtk = 0.5
        self.poisonAtk = 2.0
        self.bugAtk = 0.5
        self.dragonAtk = 0.0
        self.darkAtk = 0.5
        self.steelAtk = 2.0
