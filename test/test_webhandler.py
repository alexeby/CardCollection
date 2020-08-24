import time
import unittest

from carddatahandler.webhandler import WebHandler

if __name__ == '__main__':
    unittest.main()


class TestGetExternalCardData(unittest.TestCase):

    def test_valid_card(self):
        card_name: str = 'Kuriboh'
        card_data: dict = WebHandler.get_external_card_data_by_name(card_name)
        attack = card_data.get('atk')
        self.assertEqual(attack, 300)
        time.sleep(1)

    def test_invalid_card(self):
        card_name: str = 'Kuriboh1'
        card_data: dict = WebHandler.get_external_card_data_by_name(card_name)
        self.assertIsNone(card_data)
        time.sleep(1)

    def test_special_characters(self):
        card_name: str = '"Winged Dragon, Guardian of the Fortress #1"'
        card_data: dict = WebHandler.get_external_card_data_by_name(card_name)
        attack = card_data.get('atk')
        self.assertEqual(attack, 1400)
        time.sleep(1)


class TestDownloadImg(unittest.TestCase):

    def test_successful_img_download(self):
        # TODO
        pass