import unittest
from carddatahandler.webhandler import WebHandler
from carddatahandler.card import Card, SetInfo
import time


if __name__ == '__main__':
    unittest.main()


class TestGetExternalCardData(unittest.TestCase):

    def test_valid_card(self):
        card_name: str = 'Kuriboh'
        card_data: dict = WebHandler.get_external_card_data(card_name)
        attack = card_data.get('atk')
        self.assertEqual(attack, 300)
        time.sleep(1)

    def test_invalid_card(self):
        card_name: str = 'Kuriboh1'
        card_data: dict = WebHandler.get_external_card_data(card_name)
        self.assertIsNone(card_data)
        time.sleep(1)


class TestValidateAndAppendCardData(unittest.TestCase):

    def test_card(self):
        set_info1: SetInfo = SetInfo(set_number='STON-ENSE1', edition='LE')
        set_info2: SetInfo = SetInfo(set_number='DP04-EN012', edition='FE')
        test_card: Card = Card(name='Cyber End Dragon', race='Machine', attribute='Light',
                               monster_type='Fusion Effect Monster', level=10, attack=4000, defense=2800)
        test_card.set_set_info([set_info1, set_info2])
        external_data: dict = WebHandler.get_external_card_data(test_card.get_name())
        result_card = WebHandler.validate_and_append_card_data(test_card, external_data)
        stop = 0


class TestUsePopulatedData(unittest.TestCase):
    #TODO
    pass


class TestHandleSetData(unittest.TestCase):
    #TODO
    pass