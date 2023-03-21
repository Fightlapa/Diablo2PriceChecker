import unittest
import price_checker

import Modifier
from enums.ModifierTier import ModifierTier as ModifierTier
from enums.TargetType import TargetType as TargetType
from enums.CraftedType import CraftedType as CraftedType
from Item import Item as Item


#def calculate_for_single_mod(value: int, modifier: Modifier, item: Item):

some_caster_modifier = Modifier.Modifier("Fcr", 10, 10, ModifierTier.GOD, TargetType.CASTER, 5, 10, CraftedType.CASTER)
some_caster_only_modifier = Modifier.Modifier("Mana regen%", 0, 0, ModifierTier.GOOD, TargetType.CASTER, 4, 10, CraftedType.CASTER)
some_blood_mod = Modifier.Modifier("Strength", 1, 20, ModifierTier.GOD, TargetType.GENERAL, 1, 5, CraftedType.BLOOD)


class ExampleTests(unittest.TestCase):
    def test_curve_of_base_and_crafted_mod(self):
        item = Item()
        item.set_crafted_type(CraftedType.CASTER)
        # Possible range is 5-20, 10 base and 5-10 from crafted mod
        result5 = price_checker.calculate_for_single_mod(5, some_caster_modifier, item)
        result7 = price_checker.calculate_for_single_mod(7, some_caster_modifier, item)
        result9 = price_checker.calculate_for_single_mod(9, some_caster_modifier, item)
        result10 = price_checker.calculate_for_single_mod(10, some_caster_modifier, item)
        # result12 = price_checker.calculate_for_single_mod(12, some_caster_modifier, item) # NOT POSSIBLE!
        result15 = price_checker.calculate_for_single_mod(15, some_caster_modifier, item)
        result17 = price_checker.calculate_for_single_mod(17, some_caster_modifier, item)
        result19 = price_checker.calculate_for_single_mod(19, some_caster_modifier, item)
        result20 = price_checker.calculate_for_single_mod(20, some_caster_modifier, item)
        self.assertEqual(result5, 0.1)
        self.assertEqual(result7, 0.83)
        self.assertEqual(result9, 2.3)
        self.assertEqual(result10, 5.0)
        self.assertEqual(result15, 5.11)
        self.assertEqual(result17, 5.94)
        self.assertEqual(result19, 7.59)
        self.assertEqual(result20, 8.75)

    def test_curve_of_crafted_only_mod(self):
        item = Item()
        item.set_crafted_type(CraftedType.CASTER)
        # Possible range is 5-20, 10 base and 5-10 from crafted mod
        result4 = price_checker.calculate_for_single_mod(4, some_caster_only_modifier, item)
        result6 = price_checker.calculate_for_single_mod(6, some_caster_only_modifier, item)
        result9 = price_checker.calculate_for_single_mod(9, some_caster_only_modifier, item)
        result10 = price_checker.calculate_for_single_mod(10, some_caster_only_modifier, item)
        self.assertEqual(result4, 0.04)
        self.assertEqual(result6, 0.36)
        self.assertEqual(result9, 1.46)
        self.assertEqual(result10, 2.0)

    def test_same_mod_different_crafted_type_items_should_give_same_result(self):
        non_craft_item = Item()
        blood_item = Item()
        caster_item = Item()
        blood_item.set_crafted_type(CraftedType.BLOOD)
        caster_item.set_crafted_type(CraftedType.CASTER)

        casual_result = price_checker.calculate_for_single_mod(4, some_blood_mod, non_craft_item)
        blood_item_result = price_checker.calculate_for_single_mod(4, some_blood_mod, blood_item)
        caster_item_result = price_checker.calculate_for_single_mod(4, some_blood_mod, caster_item)

        self.assertEqual(casual_result, 0.2)
        self.assertEqual(blood_item_result, 0.2)
        self.assertEqual(caster_item_result, 0.2)




if __name__ == '__main__':
    unittest.main()