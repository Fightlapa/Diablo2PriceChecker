from enum import IntEnum


class ItemCreationState(IntEnum):
    PICK_ITEM_TYPE = 0,
    IS_ITEM_CRAFTED_QUESTION = 1,
    PICK_MOD_GROUP = 2,
    PICK_MODIFIER = 3,
    PROVIDE_VALUE = 4,
    CALCULATE = 5

    def get_previous_step(self):
        if self.value > 0:
            return ItemCreationState(self.value - 1)
        return self
    
    def get_next_step(self):
        if self.value < ItemCreationState.CALCULATE.value:
            return ItemCreationState(self.value + 1)
        return self
