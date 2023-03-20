import os
from enum import IntEnum
from typing import Dict

import Modifier
from enums.ModifierTier import ModifierTier as ModifierTier
from enums.TargetType import TargetType as TargetType
from enums.ItemCreationState import ItemCreationState as ItemCreationState
from Item import Item as Item
from enums.ItemType import ItemType as ItemType

import gui_functions
import io_functions


max_score = ModifierTier.GOD * 6

def calculate(item: Item, verbose: bool=False):
    calc_formula = lambda val, max : pow((val + 1)/(max + 1), 2)
    current_score = 0
    for modifier, value in item.get_modifiers().items():
        mapped_value = value - modifier.min
        mod_range = modifier.max - modifier.min 
        single_score = calc_formula(min(mapped_value, mod_range), mod_range) * modifier.modifier_tier
        if modifier.crafted_min != -1: # Special value for possible crafted mod
            crafted_mod_range = modifier.crafted_max - modifier.crafted_min
            if value > modifier.max: # Bonus points for combo crafted mod + normal mod
                single_score += calc_formula(value - modifier.max - modifier.crafted_min, crafted_mod_range) * modifier.modifier_tier
            elif value < modifier.min: # Bonus points for crafted modifier without casual (casual points will be always equal to 0)
                single_score += calc_formula(value - modifier.crafted_min, crafted_mod_range) * modifier.modifier_tier
        if verbose:
            print(f"Single score for mod: {modifier} with value {value} is {single_score}, out of {modifier.modifier_tier}")
        current_score += single_score
    return current_score


def print_estimate(total_score):
    print (f"Total score {total_score} out of {max_score}")
    if total_score/max_score > 0.63:
        print("Trophy I guess")
    elif total_score/max_score > 0.5:
        print("D2jsp high price I guess")
    elif total_score/max_score > 0.38:
        print("Decent for ladder I guess")
    elif total_score/max_score > 0.28:
        print("Good temp item I guess")
    else:
        print("Charsi pays good probably")
    

def main():
    current_state = ItemCreationState.PICK_ITEM_TYPE
    current_selection = 0
    current_item = Item()
    modifiers = {}

    while current_state != ItemCreationState.CALCULATE and len(list(current_item.get_modifiers().keys())) < 7:
        io_functions.clear_console()
        print(f"Current item: {current_item} Current score: {calculate(current_item)}, out of {max_score}{os.linesep}")
        if current_state == ItemCreationState.PICK_ITEM_TYPE:
            current_state, current_selection, item_type = gui_functions.select_item_type(current_state, current_selection, current_item)
            if item_type is not None:
                modifiers = Modifier.all_modifiers[item_type]
        elif current_state == ItemCreationState.IS_ITEM_CRAFTED_QUESTION:
            if current_item.item_type != ItemType.CIRCLET:
                current_state = gui_functions.fill_crafted_field(current_state, current_item)
            else:
                current_item.set_crafted(False)
                current_state = current_state.get_next_step()
        elif current_state == ItemCreationState.PICK_MOD_GROUP:
            current_state, current_selection, group = gui_functions.select_mod_group(current_state, modifiers, current_selection)
        elif current_state == ItemCreationState.PICK_MODIFIER:
            current_state, current_selection, chosen_modifier = gui_functions.select_modifier(current_state, current_selection, group, current_item)
        elif current_state == ItemCreationState.PROVIDE_VALUE:
            current_selection = 0
            current_item, current_state = gui_functions.get_modifier_value(current_item, chosen_modifier, current_state)
    total_score = calculate(current_item, True)
    print_estimate(total_score)


if __name__ == "__main__":
    main()