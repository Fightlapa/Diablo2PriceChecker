import os
from enum import IntEnum
from typing import Dict

import Modifier
from enums.ModifierTier import ModifierTier as ModifierTier
from enums.TargetType import TargetType as TargetType
from enums.ItemCreationState import ItemCreationState as ItemCreationState
from Item import Item as Item
from enums.ItemType import ItemType as ItemType
from enums.CraftedType import CraftedType as CraftedType

import gui_functions
import io_functions
import prophet_ascii


max_score = ModifierTier.GOD * 6
calc_formula = lambda val, max : round(pow((val + 1)/(max + 1), 2), 2)
full_caster_bonus = 2.0

def calculate(item: Item, verbose: bool=False):
    current_score = 0
    melee_modifiers_counter = 0 # useless for caster, used to give bonus
    for modifier, value in item.get_modifiers().items():
        single_score = calculate_for_single_mod(value, modifier, item)
        current_score += single_score
        if modifier.target_type == TargetType.MELEE:
            melee_modifiers_counter += 1
        if verbose:
            print(f"Single score for mod: {modifier} with value {value} is {single_score}, out of {modifier.modifier_tier}")
    if melee_modifiers_counter == 0:
        if verbose:
            print(f"Bonus points {full_caster_bonus} for ideal caster item")
    current_score += full_caster_bonus
    return round(current_score, 2)

def calculate_for_single_mod(value: int, modifier: Modifier.Modifier, item: Item):
    single_score = 0.0
    real_value = value - modifier.min
    mod_range = modifier.max - modifier.min # Tricky part that for 10-12 it gives 2 but there are 3 possible values
    if modifier.min != 0 and value > modifier.crafted_min and real_value >= 0: # In case of having modifier ONLY as crafted bonus, let's skip normal caclucation
        if item.get_crafted_type() != CraftedType.NONE and item.get_crafted_type() == modifier.crafted_type:
            # A few cases to consider:
            # base 10-100, crafted bonus 1-10. Having 101 means 100 base + 1 from crafted, real_value = 91, 91 - 1 >= 90 TRUE -> base = 90
            # base 10-100, crafted bonus 2-10. Having 101 means 99 base + 2 from crafted, real_value = 91, 91 - 2 >= 90 FALSE -> base = 89
            # base 10-100, crafted bonus 1-10. Having 91 means 90 base + 1 from crafted, real_value = 81, 91 - 2 >= 90 FALSE -> base = 80
            if real_value > mod_range:
                base_value = mod_range # MAX
            else:
                base_value = real_value
        else:
            base_value = real_value
        single_score = calc_formula(base_value, mod_range) * modifier.modifier_tier
    if item.get_crafted_type() != CraftedType.NONE and item.get_crafted_type() == modifier.crafted_type:
        crafted_mod_range = modifier.crafted_max - modifier.crafted_min
        # Two cases there: value exceeding base max, clearly indicating it's from crafted mod
        # Another case is value below base min value, indicating it's also from crafted mod only
        # Anything else is calculated as in base, so assuming base mod value 1-20 and crafted mod 5-10
        # having value 15, it can mean that base mod was 15 OR base is 5 and crafted is 10, the other case is a waste of crafted mod, so no bonus points
        if value > modifier.max and modifier.min != 0: # Bonus points for combo crafted mod + normal mod
            bonus_points = round(calc_formula(value - modifier.max - modifier.crafted_min, crafted_mod_range) * modifier.modifier_tier * 3 / 4, 2)
            single_score += bonus_points
            print(f"Bonus points {bonus_points} for exceeding base value by {value - modifier.max}")
        elif value < modifier.min or modifier.min == 0:
            bonus_points = round(calc_formula(value - modifier.crafted_min, crafted_mod_range) * modifier.modifier_tier * 2 / 3, 2)
            single_score += bonus_points
            print(f"Bonus points {bonus_points} for casual crafted mod {value - modifier.max}")
    return round(single_score, 2)


def print_estimate(total_score):
    print(prophet_ascii.image)
    print(f"Crystal gazer says: I'll say the score is {total_score} out of {max_score}")
    if total_score/max_score > 0.63:
        print("It's a trophy I guess")
    elif total_score/max_score > 0.5:
        print("Seek offers on d2jsp, I smell high price")
    elif total_score/max_score > 0.38:
        print("It's decent for ladder I guess")
    elif total_score/max_score > 0.28:
        print("It's good temp item I guess")
    else:
        print("I heard Charsi pays good for that")
    

def main():
    current_state = ItemCreationState.PICK_ITEM_TYPE
    current_selection = 0
    current_item = Item()
    modifiers = {}

    while current_state != ItemCreationState.CALCULATE and len(list(current_item.get_modifiers().keys())) < 7:
        io_functions.clear_console()
        print("Current item:")
        print(f"{current_item} Current score: {calculate(current_item)}, out of {max_score}{os.linesep}")
        if current_state == ItemCreationState.PICK_ITEM_TYPE:
            current_state, current_selection, item_type = gui_functions.select_item_type(current_state, current_selection, current_item)
            if item_type is not None:
                modifiers = Modifier.all_modifiers[item_type]
        elif current_state == ItemCreationState.IS_ITEM_CRAFTED_QUESTION:
            if current_item.item_type != ItemType.CIRCLET:
                current_state, current_selection = gui_functions.fill_crafted_field(current_state, current_selection, current_item)
            else:
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