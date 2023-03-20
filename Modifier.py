from enum import Enum, IntEnum

from enums.ModifierTier import ModifierTier as ModifierTier
from enums.TargetType import TargetType as TargetType
from enums.ItemType import ItemType as ItemType

class TargetType(IntEnum):
    CASTER = 1,
    MELEE = 2,
    GENERAL = 3

    
class ModifierClass(str, Enum):
    RESISTS = "Resists",
    STATS = "Stats",
    CASTER = "Caster(fc/mana reg)",
    MELEE = "Melee",
    MF_LEECH_GOLD = "Mf/leech/gold",
    OTHER = "Other"


class Modifier():
    target_type: TargetType
    min: int
    max: int
    modifier_tier: ModifierTier
    name: str
    
    crafted_min: int = -1
    crafted_max: int = -1

    def __init__(self,
                 name: str,
                 min: int,
                 max: int,
                 modifier_tier: ModifierTier,
                 target_type: TargetType,
                 crafted_min: int = -1,
                 crafted_max: int = -1):
        self.name = name
        self.min = min
        self.max = max
        self.modifier_tier = modifier_tier
        self.target_type = target_type
        self.crafted_min = crafted_min
        self.crafted_max = crafted_max

    def __str__(self):
        return f"{self.name}: {self.min} - {self.max}"

    def __repr__(self):
        return self.__str__()
    
all_modifiers = {
    ItemType.RING: {
        "Resists":[
            Modifier("All resistances", 3, 11, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Lightning resistance", 5, 30, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Fire resistance", 5, 30, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Cold resistance", 5, 30, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Poison resistance", 5, 30, ModifierTier.MEDIUM, TargetType.GENERAL),
        ],
        "Stats":[
            Modifier("Strength", 1, 20, ModifierTier.GOD, TargetType.GENERAL, 1, 5),
            Modifier("Dexterity", 1, 15, ModifierTier.MEDIUM, TargetType.GENERAL, 1, 5),
            Modifier("Energy", 1, 15, ModifierTier.GOOD, TargetType.GENERAL, 1, 5),
            Modifier("Life", 1, 40, ModifierTier.GOD, TargetType.GENERAL, 10, 20),
            Modifier("Mana", 1, 90, ModifierTier.GOOD, TargetType.GENERAL, 10, 20),
            Modifier("Vitality", -1, -1, ModifierTier.GOD, TargetType.GENERAL, 1, 5),
        ],
        "Caster(fcr/mana reg)":[
            Modifier("Fcr", 10, 10, ModifierTier.GOD, TargetType.CASTER),
            Modifier("Mana regen%", -1, -1, ModifierTier.GOOD, TargetType.CASTER, 4, 10)
        ],
        "Melee":[
            Modifier("Attack rating", 10, 150,  ModifierTier.GOD_OVERLAPPING, TargetType.MELEE),
            Modifier("Attack rating%", 5, 5,  ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Minimum damage", 1, 9, ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Maximum damage", 1, 12, ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Fire damage(max)", 2, 6, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Cold damage(max)", 1, 2, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Lightning damage(max)", 6, 23, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Poison damage(max)", 1, 50, ModifierTier.LOW, TargetType.MELEE),
        ],
        "Mf/leech/gold":[
            Modifier("Life leech%", 2, 9, ModifierTier.GOD, TargetType.MELEE, 1, 3),
            Modifier("Mana leech%", 2, 9, ModifierTier.GOD, TargetType.MELEE),
            Modifier("Extra gold%", 25, 40, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Mf%", 5, 15, ModifierTier.GOOD, TargetType.GENERAL),
        ],
        "Other":[
            Modifier("Life regen", 3, 10, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Damage reduction", 1, 2, ModifierTier.LOW, TargetType.GENERAL, 1, 4),
            Modifier("Magic damage reduction", 1, 2, ModifierTier.LOW, TargetType.MELEE, 1, 2),
            Modifier("Half freeze duration", 1, 1, ModifierTier.LOW, TargetType.GENERAL),
        ]
    },
    ItemType.AMULET: {
        "Resists":[
            Modifier("All resistances", 3, 20, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Lightning resistance", 5, 40, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Fire resistance", 5, 40, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Cold resistance", 5, 40, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Poison resistance", 5, 40, ModifierTier.MEDIUM, TargetType.GENERAL),
        ],
        "Stats":[
            Modifier("Strength", 1, 30, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Dexterity", 1, 20, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Energy", 1, 20, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Life", 1, 60, ModifierTier.GOD, TargetType.GENERAL, 10, 20),
            Modifier("Mana", 1, 90, ModifierTier.GOOD, TargetType.GENERAL, 10, 20)
        ],
        "Skills": [
            Modifier("OP skill tree", 1, 2, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Decent skill tree", 1, 2, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Mleh skill tree", 1, 2, ModifierTier.LOW, TargetType.GENERAL),
            Modifier("All skills OP class", 1, 2, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("All skills casual class", 1, 2, ModifierTier.GOOD, TargetType.GENERAL)
        ],
        "Caster(fcr/mana reg)":[
            Modifier("Fcr", 10, 10, ModifierTier.GOD, TargetType.CASTER, 5, 10),
            Modifier("Mana regen%", -1, -1, ModifierTier.GOOD, TargetType.CASTER, 4, 10)
        ],
        "Melee":[
            Modifier("Attack rating", 10, 150,  ModifierTier.GOD_OVERLAPPING, TargetType.MELEE),
            Modifier("Attack rating%", 5, 5,  ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Minimum damage", 1, 9, ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Maximum damage", 1, 12, ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Fire damage(max)", 2, 6, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Cold damage(max)", 1, 2, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Lightning damage(max)", 6, 23, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Poison damage(max)", 1, 50, ModifierTier.LOW, TargetType.MELEE),
        ],
        "Mf/leech/gold":[
            Modifier("Life leech%", 2, 9, ModifierTier.GOD, TargetType.MELEE, 1, 4),
            Modifier("Mana leech%", 2, 9, ModifierTier.GOD, TargetType.MELEE),
            Modifier("Extra gold%", 25, 80, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Mf%", 5, 25, ModifierTier.GOOD, TargetType.GENERAL),
        ],
        "Other":[
            Modifier("Life regen", 3, 10, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Damage reduction", 1, 7, ModifierTier.LOW, TargetType.GENERAL),
            Modifier("Magic damage reduction", 1, 3, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Half freeze duration", 1, 1, ModifierTier.LOW, TargetType.GENERAL),
            Modifier("Faster run walk", -1, -1, ModifierTier.MEDIUM, TargetType.GENERAL, 5, 10),
        ]
    },
    ItemType.CIRCLET: {
        "Resists":[
            Modifier("All resistances", 3, 20, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Lightning resistance", 5, 40, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Fire resistance", 5, 40, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Cold resistance", 5, 40, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Poison resistance", 5, 40, ModifierTier.MEDIUM, TargetType.GENERAL),
        ],
        "Stats":[
            Modifier("Strength", 1, 30, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Dexterity", 1, 20, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Energy", 1, 20, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Life", 1, 60, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Mana", 6, 90, ModifierTier.GOOD, TargetType.GENERAL)
        ],
        "Skills": [
            Modifier("OP skill tree", 1, 2, ModifierTier.GOOD, TargetType.GENERAL),
            Modifier("Decent skill tree", 1, 2, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Mleh skill tree", 1, 2, ModifierTier.LOW, TargetType.GENERAL),
            Modifier("All skills OP class", 1, 2, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("All skills casual class", 1, 2, ModifierTier.GOOD, TargetType.GENERAL)
        ],
        "FCR":[
            Modifier("Fcr * 10%", 1, 2, ModifierTier.GOD, TargetType.CASTER),
        ],
        "Melee":[
            Modifier("Attack rating", 10, 120,  ModifierTier.GOD, TargetType.MELEE),
            Modifier("Attack rating%", 5, 5,  ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Enhanced damage%", 10, 30,  ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Minimum damage", 1, 9, ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Maximum damage", 1, 12, ModifierTier.GOOD, TargetType.MELEE),
            Modifier("Fire damage(max)", 31, 60, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Cold damage(max)", 19, 30, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Lightning damage(max)", 49, 120, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Poison damage(max)", 1, 50, ModifierTier.LOW, TargetType.MELEE),
        ],
        "Mf/leech/gold":[
            Modifier("Life leech%", 2, 9, ModifierTier.GOD, TargetType.MELEE),
            Modifier("Mana leech%", 2, 9, ModifierTier.GOD, TargetType.MELEE),
            Modifier("Extra gold%", 25, 80, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Mf%", 5, 25, ModifierTier.GOOD, TargetType.GENERAL),
        ],
        "Other":[
            Modifier("Sockets", 1, 2, ModifierTier.GOD, TargetType.GENERAL),
            Modifier("Life regen", 3, 10, ModifierTier.MEDIUM, TargetType.GENERAL),
            Modifier("Damage reduction", 1, 7, ModifierTier.LOW, TargetType.GENERAL),
            Modifier("Magic damage reduction", 1, 3, ModifierTier.LOW, TargetType.MELEE),
            Modifier("Half freeze duration", 1, 1, ModifierTier.LOW, TargetType.GENERAL),
            Modifier("Faster run walk * 10%", 1, 3, ModifierTier.GOD, TargetType.GENERAL),
        ]
    }
}