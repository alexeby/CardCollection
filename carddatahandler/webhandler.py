import bs4
import requests
import logging
from carddatahandler.card import Card, SetInfo
from urllib.parse import quote
import json
from typing import List
import time

logger = logging.getLogger(__name__)

# TODO use config file


class WebHandler:

    def __init__(self):
        pass

    @staticmethod
    def get_external_card_data_by_name(card_name: str):
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

