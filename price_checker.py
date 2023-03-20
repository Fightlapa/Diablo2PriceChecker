import os
from enum import IntEnum
from typing import Dict

from Modifier import Modifier as Modifier
from ModifierTier import ModifierTier as ModifierTier
from TargetType import TargetType as TargetType
from ItemCreationState import ItemCreationState as ItemCreationState
from Item import Item as Item

import gui_functions
import io_functions


max_score = ModifierTier.GOD * 6

ring_mods = {
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
        Modifier("Energy", 1, 15, ModifierTier.LOW, TargetType.GENERAL, 1, 5),
        Modifier("Life", 1, 40, ModifierTier.GOD, TargetType.GENERAL, 10, 20),
        Modifier("Mana", 1, 90, ModifierTier.GOD, TargetType.GENERAL, 10, 20),
        Modifier("Vitality", -1, -1, ModifierTier.GOD, TargetType.GENERAL, 1, 5),
    ],
    "Caster(fcr/mana reg)":[
        Modifier("Fcr", 10, 10, ModifierTier.GOD, TargetType.CASTER),
        Modifier("Mana regen%", -1, -1, ModifierTier.GOOD, TargetType.CASTER, 4, 10)
    ],
    "Melee":[
        Modifier("Attack rating", 10, 120,  ModifierTier.GOD, TargetType.MELEE),
        Modifier("Minimal damage", 1, 14, ModifierTier.GOOD, TargetType.MELEE),
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
        Modifier("Half freeze duration", 1, 2, ModifierTier.LOW, TargetType.GENERAL),
    ]
}

def calculate(item: Item, verbose: bool=False):
    calc_formula = lambda val, max : pow((val + 1)/(max + 1), 2)
    current_score = 0
    for modifier, value in item.get_modifiers().items():
        mapped_value = value - modifier.min
        mod_range = modifier.max - modifier.min 
        single_score = calc_formula(mapped_value, mod_range) * modifier.modifier_tier
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
    elif total_score/max_score > 0.4:
        print("Decent for ladder I guess")
    elif total_score/max_score > 0.3:
        print("Good temp ring I guess")
    else:
        print("Charsi pays good probably")
    

def main():
    current_state = ItemCreationState.IS_ITEM_CRAFTED_QUESTION
    current_selection = 0
    current_ring = Item()

    while current_state != ItemCreationState.CALCULATE and len(list(current_ring.get_modifiers().keys())) < 7:
        io_functions.clear_console()
        print(f"Current ring: {current_ring} Current score: {calculate(current_ring)}, out of {max_score}{os.linesep}")
        if current_state == ItemCreationState.IS_ITEM_CRAFTED_QUESTION:
            current_state = gui_functions.fill_crafted_field(current_state, current_ring)
        elif current_state == ItemCreationState.PICK_MOD_GROUP:
            current_state, current_selection, group = gui_functions.select_mod_group(current_state, ring_mods, current_selection)
        elif current_state == ItemCreationState.PICK_MODIFIER:
            current_state, current_selection, chosen_modifier = gui_functions.select_modifier(current_state, current_selection, group, current_ring)
        elif current_state == ItemCreationState.PROVIDE_VALUE:
            current_selection = 0
            current_ring, current_state = gui_functions.get_modifier_value(current_ring, chosen_modifier, current_state)
    total_score = calculate(current_ring, True)
    print_estimate(total_score)


if __name__ == "__main__":
    main()