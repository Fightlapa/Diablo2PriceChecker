from enum import Enum


class CraftedType(str, Enum):
    NONE = "Not crafted",
    CASTER = "Caster",
    BLOOD = "Blood"