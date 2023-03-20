from enum import Enum
from typing import Dict, Optional
import os

from Modifier import Modifier as Modifier
from enums.ItemType import ItemType as ItemType


class Item():
    modifiers: Dict[Modifier, int] = {}
    item_type: ItemType
    crafted: Optional[bool] = None

    def set_crafted(self, value: bool):
        self.crafted = value

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    def get_modifiers(self):
        return self.modifiers
    
    def is_crafted(self) -> bool:
        return self.crafted
    
    def set_item_type(self, item_type: ItemType):
        self.item_type = item_type

    def __str__(self):
        print_str = ""
        if self.crafted is not None:
            print_str += f"Crafted: {self.crafted} {os.linesep}"
        for modifier, value in self.get_modifiers().items():
            print_str += f"{modifier.name.ljust(23)}[{modifier.min}  -  {modifier.max}]\t-  {value}{os.linesep}"
        return print_str
