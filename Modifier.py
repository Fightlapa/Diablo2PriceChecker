from enum import IntEnum

from ModifierTier import ModifierTier as ModifierTier
from TargetType import TargetType as TargetType

class TargetType(IntEnum):
    CASTER = 1,
    MELEE = 2,
    GENERAL = 3


class Modifier():
    target_type: TargetType
    min: int
    max: int
    modifier_tier: ModifierTier
    name: str
    crafted_min: int = 0
    crafted_max: int = 0

    def __init__(self, name: str, min: int, max: int, modifier_tier: ModifierTier, target_type: TargetType, crafted_min: int = 0, crafted_max: int = 0):
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