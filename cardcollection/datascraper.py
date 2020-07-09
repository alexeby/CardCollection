import bs4
import requests
import logging
import configparser
from cardcollection.card import Card, SetInfo
from urllib.parse import quote
import json

logger = logging.getLogger(__name__)

# Initialize browser driver
# TODO use config file


class DataScraper:

    def __init__(self):
        pass

    @staticmethod
    def validate_card_data():
        pass

    @staticmethod
    def get_external_card_data(card: Card):
        card_name = quote(card.get_name())
        url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?name=' + card_name
        site = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        content = bs4.BeautifulSoup(site.text, 'html.parser')

        json_data = json.loads(content.prettify())
        return json_data['data'][0]

    @staticmethod
    def execute(card_list: list):
        for card in card_list:
            card_data: dict = DataScraper.get_external_card_data(card)

