import json
import logging
from urllib.parse import quote

import bs4
import requests

from carddatahandler import WEB_HANDLER_PROPERTIES, PATHS_PROPERTIES

logger = logging.getLogger(__name__)


class WebHandler:

    def __init__(self):
        pass

    @staticmethod
    def get_external_card_data_by_name(card_name: str):
        # TODO documentation
        card_name_quote = quote(card_name)
        url = WEB_HANDLER_PROPERTIES.get('card_search_site_api') + card_name_quote
        site = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if site.status_code == 200:
            content = bs4.BeautifulSoup(site.text, 'html.parser')
            json_data = json.loads(content.prettify())
            return json_data['data'][0]
        logger.error('Error when retrieving card '+card_name+'. Status code: '+site.status_code.__str__())
        return None

    @staticmethod
    def download_img(url: str, img_name: str):
        # TODO documentation
        # TODO testing
        # File path of where you want to save the image
        file_path = PATHS_PROPERTIES.get('img_download_dir')
        full_path = file_path + img_name

        # Download the image by opening the file in 'Write Binary' mode
        download_link = requests.get(url)
        with open(full_path, "wb") as img_object:
            img_object.write(download_link.content)


