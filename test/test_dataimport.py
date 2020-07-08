import unittest
from cardcollection.dataimport import DataImport
from cardcollection.card import SetInfo
from cardcollection.card import Card
from typing import List


class TestGetKeyFromValue(unittest.TestCase):

    def test_key_is_found(self):
        dictionary: dict = {'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0}
        key = DataImport.get_key_from_value(dictionary, 1)
        self.assertEqual(key, 'NM')

    def test_key_is_not_found(self):
        dictionary: dict = {'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0}
        key = DataImport.get_key_from_value(dictionary, 3)
        self.assertEqual(key, None)


class TestIndexOfExistingData(unittest.TestCase):

    def test_card_exists(self):
        new_card = Card(name='This is a card')
        card_list: List[Card] = []
        card_list.append(Card(name='This is another card'))
        card_list.append(Card(name='This is yet another card'))
        card_list.append(Card(name='This is a card'))
        card_list.append(Card(name='This is a final card'))
        result = DataImport.index_of_existing_data(new_card, card_list)
        self.assertEqual(result, 2)

    def test_card_not_exists(self):
        new_card = Card(name='This is a card')
        card_list: List[Card] = []
        card_list.append(Card(name='This is another card'))
        card_list.append(Card(name='This is yet another card'))
        card_list.append(Card(name='This is a final card'))
        result = DataImport.index_of_existing_data(new_card, card_list)
        self.assertEqual(result, None)


class TestHandleConditions(unittest.TestCase):

    def test_handle_conditions_add(self):
        conditions: dict = {'NM': 2, 'D': 0}
        new_condition = 'D'
        updated_conditions = DataImport.handle_conditions(conditions, new_condition)
        self.assertEqual(updated_conditions, {'NM': 2, 'D': 1})

    def test_handle_conditions_not_exist(self):
        conditions: dict = {'NM': 2, 'D': 0}
        new_condition = 'RE'
        updated_conditions = DataImport.handle_conditions(conditions, new_condition)
        self.assertEqual(updated_conditions, conditions)


class TestDoSetsMatch(unittest.TestCase):

    def test_sets_do_match(self):
        set1: SetInfo = SetInfo(set_number='CDIP-EN035', edition='FE')
        set2: SetInfo = SetInfo(set_number='CDIP-EN035', edition='FE')
        result = DataImport.do_sets_match(set1, set2)
        self.assertTrue(result)

    def test_sets_do_not_match(self):
        set1: SetInfo = SetInfo(set_number='STON-ENSE1', edition='LE')
        set2: SetInfo = SetInfo(set_number='DP04-EN012', edition='FE')
        result = DataImport.do_sets_match(set1, set2)
        self.assertFalse(result)

    def test_sets_partial_match(self):
        set1: SetInfo = SetInfo(set_number='STON-ENSE1', edition='LE')
        set2: SetInfo = SetInfo(set_number='STON-ENSE1', edition='FE')
        result = DataImport.do_sets_match(set1, set2)
        self.assertFalse(result)

        set1: SetInfo = SetInfo(set_number='STON-ENSE1', edition='FE')
        set2: SetInfo = SetInfo(set_number='DP04-EN012', edition='FE')
        result = DataImport.do_sets_match(set1, set2)
        self.assertFalse(result)


class TestInitIndexes(unittest.TestCase):

    def test_init_indexes(self):
        header = ['name', 'monster_type', 'attribute', 'level', 'attack', 'defense', 'pass_code',
                  'description', 'set_number', 'edition', 'rarity', 'condition']
        result = DataImport.init_indexes(header)
        self.assertEqual(result.get('attack'), 4)
        self.assertEqual(result.get('edition'), 9)

    def test_init_indexes_not_registered(self):
        header = ['name', 'monster_type', 'attributes', 'level', 'attack', 'defense', 'pass_code',
                  'description', 'set_number', 'edition', 'rarity', 'condition']
        result = DataImport.init_indexes(header)
        self.assertEqual(result.get('attributes'), None)
        self.assertEqual(result.get('rarity'), 10)


class TestDefineCardObject(unittest.TestCase):

    def test_define_card_object(self):
        header = ['name', 'monster_type', 'attribute', 'level', 'attack', 'defense', 'edition',
                  'set_number', 'pass_code', 'condition']
        indexes = DataImport.init_indexes(header)
        card_info = ['Blue-Eyes White Dragon', 'Dragon', 'Light', 8, '3000', '2500', None,
                     'SDK-001', '89631139', 'LP']

        card_object = DataImport.define_card_object(indexes, card_info)
        predefined_set_object = SetInfo(set_number='SDK-001', conditions={'NM': 0, 'LP': 1, 'MP': 0, 'HP': 0, 'D': 0})
        predefined_card_object = Card(name='Blue-Eyes White Dragon', monster_type='Dragon', attribute='Light',
                                      level=8, attack='3000', defense='2500', pass_code='89631139',
                                      set_info=[predefined_set_object])
        self.assertEqual(card_object, predefined_card_object)


class TestHandleSetInfo(unittest.TestCase):

    def test_different_sets(self):
        new_set_info = SetInfo(set_number='STON-ENSE1', conditions={'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0},
                               edition='LE')
        new_card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[new_set_info])
        existing_set_info = SetInfo(set_number='DP04-EN012', conditions={'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0},
                                    edition='FE')
        existing_card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[existing_set_info])

        result_card = DataImport.handle_set_info(new_card, existing_card)

        expected_card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[existing_set_info, new_set_info])

        self.assertEqual(result_card, expected_card)

    def test_same_sets(self):
        set_info = SetInfo(set_number='STON-ENSE1', conditions={'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0},
                           edition='LE')
        card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[set_info])

        result_card = DataImport.handle_set_info(card, card)

        expected_set_info = SetInfo(set_number='STON-ENSE1', conditions={'NM': 2, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0},
                                    edition='LE')
        expected_card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[expected_set_info])

        self.assertEqual(result_card, expected_card)

    def test_similar_sets(self):
        set_info1 = SetInfo(set_number='STON-ENSE1', conditions={'NM': 0, 'LP': 0, 'MP': 0, 'HP': 1, 'D': 0},
                            edition='LE')
        card1 = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[set_info1])

        set_info2 = SetInfo(set_number='STON-ENSE1', conditions={'NM': 1, 'LP': 1, 'MP': 0, 'HP': 0, 'D': 0},
                           edition='LE')
        card2 = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                    level=10, attack='4000', defense='2800', pass_code='1546123',
                    set_info=[set_info2])

        result_card = DataImport.handle_set_info(card1, card2)

        expected_set_info = SetInfo(set_number='STON-ENSE1', conditions={'NM': 1, 'LP': 1, 'MP': 0, 'HP': 1, 'D': 0},
                                    edition='LE')
        expected_card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                                      level=10, attack='4000', defense='2800', pass_code='1546123',
                                      set_info=[expected_set_info])

        self.assertEqual(result_card, expected_card)

    def test_same_set_different_editions(self):
        set_info1 = SetInfo(set_number='STON-ENSE1', conditions={'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0},
                           edition='LE')
        card1 = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                    level=10, attack='4000', defense='2800', pass_code='1546123',
                    set_info=[set_info1])

        set_info2 = SetInfo(set_number='STON-ENSE1', conditions={'NM': 0, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 1},
                           edition=None)
        card2 = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                    level=10, attack='4000', defense='2800', pass_code='1546123',
                    set_info=[set_info2])

        result_card = DataImport.handle_set_info(card1, card2)

        expected_set_info1 = SetInfo(set_number='STON-ENSE1', conditions={'NM': 1, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 0},
                                    edition='LE')
        expected_set_info2 = SetInfo(set_number='STON-ENSE1', conditions={'NM': 0, 'LP': 0, 'MP': 0, 'HP': 0, 'D': 1},
                                     edition=None)
        expected_card = Card(name='Cyber End Dragon', monster_type='Machine / Fusion / Effect', attribute='Light',
                             level=10, attack='4000', defense='2800', pass_code='1546123',
                             set_info=[expected_set_info2, expected_set_info1])

        self.assertEqual(result_card, expected_card)
