import unittest
from cardcollection.dataimport import DataImport
from cardcollection.card import Card


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
        card_list = []
        card_list.append(Card(name='This is another card'))
        card_list.append(Card(name='This is yet another card'))
        card_list.append(Card(name='This is a card'))
        card_list.append(Card(name='This is a final card'))
        result = DataImport.index_of_existing_data(new_card, card_list)
        self.assertEqual(result, 2)
