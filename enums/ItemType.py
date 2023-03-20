from enum import Enum


class ItemType(str, Enum):
    RING = "Ring",
    AMULET = "Amulet",
    CIRCLET = "Circlet"