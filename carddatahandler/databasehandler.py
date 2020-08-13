from carddatahandler.card import Card, SetInfo
from typing import List
from pymongo import MongoClient
import logging

logger = logging.getLogger(__name__)

class DatabaseHandler:

    def __init__(self):
        pass

    @staticmethod
    def convert_card_to_dict(card: Card):
        # Handle set information before card data because set will append to card
        card_set_info: List[SetInfo] = card.get_set_info()
        card_set_dict: dict = {}
        for card_set in card_set_info:
            set_number = card_set.get_set_number()
            set_dict = {
                'edition': card_set.get_edition(),
                'rarity': card_set.get_rarity(),
                'price': card_set.get_price(),
                'conditions': card_set.get_conditions()
            }
            card_set_dict[set_number] = set_dict

        # Handle card information and append set info dictionary
        card_dict = {
            'name': card.get_name(),
            'monster_type': card.get_monster_type(),
            'attribute': card.get_attribute(),
            'race': card.get_race(),
            'level': card.get_level(),
            'attack': card.get_attack(),
            'defense': card.get_defense(),
            'pass_code': card.get_pass_code(),
            'description': card.get_description(),
            'img_name': card.get_img_name(),
            'last_process_date': card.get_last_process_date(),
            'set_info': card_set_dict
        }

        return card_dict

    @staticmethod
    def convert_cards_to_dicts(cards: List[Card]):
        dict_card_list: List[dict] = []
        for card in cards:
            dict_card = DatabaseHandler.convert_card_to_dict(card)
            dict_card_list.append(dict_card)

        return dict_card_list

    @staticmethod
    def persist_record_to_collection(record: dict):
        mongo_client = MongoClient('MONGOCONNECTIONURL')
        if mongo_client is None:
            logger.error('MongoDB Client could not be initialized')
            return None
        try:
            db = mongo_client['DATABASE']
            collection = db['COLLECTION']
            collection.insert_one(record)
        except:
            logger.error('Error connecting to database')

    @staticmethod
    def persist_multiple_records_to_collection(records: List[dict]):
        mongo_client = MongoClient('MONGOCONNECTIONURL')
        if mongo_client is None:
            logger.error('MongoDB Client could not be initialized')
            return None
        try:
            db = mongo_client['DATABASE']
            collection = db['COLLECTION']
            collection.insert_many(records)
        except:
            logger.error('Error connecting to database')