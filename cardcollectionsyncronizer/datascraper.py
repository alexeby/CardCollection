import bs4
import requests
import logging
from cardcollectionsyncronizer.card import Card, SetInfo
from urllib.parse import quote
import json
from typing import List
import time

logger = logging.getLogger(__name__)

# TODO use config file


class DataScraper:

    def __init__(self):
        pass

    @staticmethod
    def handle_set_data(external_card_sets: List[dict], card_sets: List[SetInfo]):
        card_set: SetInfo
        for card_set in card_sets:
            external_card_set: dict
            for external_card_set in external_card_sets:
                if card_set.get_set_number() == external_card_set.get('set_code'):
                    card_set.set_price(DataScraper.use_populated_data(card_set.get_price(), external_card_set.get('set_price')))
                    card_set.set_rarity(DataScraper.use_populated_data(card_set.get_rarity(), external_card_set.get('set_rarity')))

        return card_sets

    @staticmethod
    def use_populated_data(card_object_data: str, card_external_data: str):
        if card_object_data == card_external_data:
            # Card data equals, no need to validate
            return card_object_data
        if card_object_data != card_external_data:
            if card_object_data is None:
                # Card object is not populated, but external data is
                return card_external_data
            elif card_external_data is None:
                # External data is not populated, but card object is
                return card_object_data
            # Always use card data from csv, and log to verify the discrepancy
            logger.warning(card_object_data + ' is not ' + card_external_data)
            return card_object_data
        return None

    @staticmethod
    def validate_and_append_card_data(card: Card, card_data: dict):
        card.set_name(DataScraper.use_populated_data(card.get_name(), card_data.get('name')))
        card.set_level(DataScraper.use_populated_data(card.get_level(), card_data.get('level')))
        card.set_attack(DataScraper.use_populated_data(card.get_attack(), card_data.get('atk')))
        card.set_defense(DataScraper.use_populated_data(card.get_defense(), card_data.get('def')))
        card.set_description(DataScraper.use_populated_data(card.get_description(), card_data.get('desc')))
        card.set_attribute(DataScraper.use_populated_data(card.get_attribute(), card_data.get('attribute')))
        card.set_monster_type(DataScraper.use_populated_data(card.get_monster_type(), card_data.get('type')))

        set_info: List[SetInfo] = DataScraper.handle_set_data(card_data.get('card_sets'), card.get_set_info())
        card.set_set_info(set_info)

        return card

    @staticmethod
    # Tested
    def get_external_card_data(card_name: str):
        card_name_quote = quote(card_name)
        # TODO config file
        url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=' + card_name_quote
        site = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if site.status_code == 200:
            content = bs4.BeautifulSoup(site.text, 'html.parser')

            json_data = json.loads(content.prettify())
            return json_data['data'][0]
        logger.error('Error when retrieving card '+card_name+'. Status code: '+site.status_code.__str__())
        return None

    @staticmethod
    def execute(card_list: List[Card]):
        i: int = 0
        card: Card
        for card in card_list:
            card_name = card.get_name()
            card_data: dict = DataScraper.get_external_card_data(card_name)
            card = DataScraper.validate_and_append_card_data(card, card_data)
            card_list[i] = card
            i = i + 1
            time.sleep(1)
        return card_list
