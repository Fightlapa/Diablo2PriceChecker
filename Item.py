from enum import Enum
from typing import Dict, Optional
import os

from Modifier import Modifier as Modifier
from enums.ItemType import ItemType as ItemType
from enums.CraftedType import CraftedType as CraftedType


class Item():
    modifiers: Dict[Modifier, int] = {}
    item_type: ItemType
    crafted_type: Optional[CraftedType] = None

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    def get_modifiers(self) ->  Dict[Modifier, int]:
        return self.modifiers
    
    def set_item_type(self, item_type: ItemType):
        self.item_type = item_type

    def set_crafted_type(self, crafted_type: CraftedType):
        self.crafted_type = crafted_type

    def get_crafted_type(self) -> Optional[CraftedType]:
        return self.crafted_type

    def __str__(self):
        print_str = ""
        if self.crafted_type != CraftedType.NONE:
            print_str += f"Crafted: {self.crafted_type} {os.linesep}"
        for modifier, value in self.get_modifiers().items():
            print_str += f"{modifier.name.ljust(23)}[{modifier.min}  -  {modifier.max}]\t-  {value}{os.linesep}"
        return print_str
