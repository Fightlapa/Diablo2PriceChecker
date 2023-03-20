import os

from typing import Dict, List
import io_functions

from Modifier import Modifier as Modifier
from enums.ItemCreationState import ItemCreationState as ItemCreationState
from Item import Item as Item
from enums.ItemType import ItemType as ItemType

def show_options(options: List, current_selection: int):
    for i in range(0, len(options)):
        to_print = ""
        if current_selection == i:
            to_print += "-->"
        to_print += options[i]
        print(to_print)
    print_special_actions()

def print_special_actions():
    print(f"{os.linesep}Press 'q' to proceed to calculation")
    print(f"Press 'b' to go back")

def get_modifier_value(current_item: Item, chosen_modifier: Modifier, current_state: ItemCreationState):
    success = False
    value = None
    print_special_actions()
    while not success:
        min_val = chosen_modifier.min
        max_val = chosen_modifier.max
        if current_item.is_crafted() and chosen_modifier.crafted_min != -1: # Special value for no crafted mod
            min_val = min(chosen_modifier.crafted_min, chosen_modifier.min)
            max_val += chosen_modifier.crafted_max
        if min_val == max_val:
            value = min_val
            break
        try:
            user_input = input(f"Write value {chosen_modifier.name} [{min_val} - {max_val}] and press enter: ")
            if user_input == io_functions.K_Q.decode():
                current_state = ItemCreationState.CALCULATE
                break
            elif user_input == io_functions.K_B.decode():
                current_state = current_state.get_previous_step()
            else:
                value = int(user_input)
            if value is not None:
                if value < min_val or value > max_val:
                    value = None
                    continue
            success = True
        except Exception as _:
            print("Try again...")
    if value is not None:
        current_item.get_modifiers()[chosen_modifier] = value
        current_state = ItemCreationState.PICK_MOD_GROUP
    return current_item, current_state


def change_selection_if_applicaple(key, options_to_print: List, current_selection):
    if key == io_functions.K_UP:
        current_selection -= 1
    if key == io_functions.K_DOWN:
        current_selection += 1
    if current_selection < 0:
        current_selection = 0
    if current_selection > (len(options_to_print) - 1):
        current_selection = len(options_to_print) - 1
    return current_selection

def select_mod_group(current_state: ItemCreationState, modifiers_pool: Dict[str, Modifier], current_selection: int):
    group = None
    options_to_print = list(modifiers_pool.keys())
    show_options(options_to_print, current_selection)
    key = io_functions.get_selection_input()
    if key == io_functions.K_Q:
        current_state = ItemCreationState.CALCULATE
    elif key == io_functions.K_B:
        current_selection = 0
        current_state = current_state.get_previous_step()
    else:
        current_selection = change_selection_if_applicaple(key, options_to_print, current_selection)
        if key == io_functions.K_ENTER:
            group = modifiers_pool[options_to_print[current_selection]]
            current_state = current_state.get_next_step()
            current_selection = 0
    return current_state, current_selection, group

def select_item_type(current_state: ItemCreationState, current_selection: int, current_item: Item):
    item_type = None
    options_to_print = [item_type for item_type in ItemType]
    show_options(options_to_print, current_selection)
    key = io_functions.get_selection_input()
    if key == io_functions.K_Q:
        current_state = ItemCreationState.CALCULATE
    elif key == io_functions.K_B:
        current_selection = 0
        current_state = current_state.get_previous_step()
    else:
        current_selection = change_selection_if_applicaple(key, options_to_print, current_selection)
        if key == io_functions.K_ENTER:
            item_type = options_to_print[current_selection]
            current_item.set_item_type(item_type)
            current_state = current_state.get_next_step()
            current_selection = 0
    return current_state, current_selection, item_type

def select_modifier(current_state: ItemCreationState, current_selection: int, group, item: Item):
    chosen_modifier = None
    options_to_print = [modifier.name for modifier in group if item.is_crafted() or (not item.is_crafted() and modifier.min != -1)]
    show_options(options_to_print, current_selection)
    key = io_functions.get_selection_input()
    if key == io_functions.K_Q:
        current_state = ItemCreationState.CALCULATE
    elif key == io_functions.K_B:
        current_state = current_state.get_previous_step()
        current_selection = 0
    else:
        current_selection = change_selection_if_applicaple(key, options_to_print, current_selection)
        if key == io_functions.K_ENTER:
            chosen_modifier = group[current_selection]
            current_state = current_state.get_next_step()
            current_selection = 0
    return current_state, current_selection, chosen_modifier


def fill_crafted_field(current_state: ItemCreationState, item: Item):
    print("Is item crafted? y/n:")
    key = io_functions.get_yes_no_input()
    if key == io_functions.K_N:
        item.set_crafted(False)
        current_state = current_state.get_next_step()
    elif key == io_functions.K_Y:
        item.set_crafted(True)
        current_state = current_state.get_next_step()
    elif key == io_functions.K_B:
        current_state = current_state.get_previous_step()
    return current_state