from enum import IntEnum


class ModifierTier(IntEnum):
    LOW = 1,
    MEDIUM = 2,
    GOOD = 3,
    VERY_GOOD = 4,
    GOD = 5,
    GOD_OVERLAPPING = 8 # in case of attack rating, two mods give bonus, so extra points for style