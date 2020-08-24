import logging
from typing import List

from pymongo import MongoClient, errors

from carddatahandler import DATABASE_HANDLER_PROPERTIES
from carddatahandler.card import Card, SetInfo

logger = logging.getLogger(__name__)

CLIENT = DATABASE_HANDLER_PROPERTIES.get('mongodb_client')
DATABASE = DATABASE_HANDLER_PROPERTIES.get('database')
COLLECTION = DATABASE_HANDLER_PROPERTIES.get('collection')
TIMEOUT = int(DATABASE_HANDLER_PROPERTIES.get('timeout'))


class DatabaseHandler:

    def __init__(self):
        pass

    @staticmethod
    def convert_card_to_dict(card: Card):
        # TODO documentation
        # TODO testing
        # Handle set information before card data because set will append to card
        card_set_info: List[SetInfo] = card.get_set_info()
        card_set_list: List[dict] = []
        for card_set in card_set_info:
            set_dict = {
                'set_number': card_set.get_set_number(),
                'edition': card_set.get_edition(),
                'rarity': card_set.get_rarity(),
                'price': card_set.get_price(),
                'conditions': card_set.get_conditions()
            }
            card_set_list.append(set_dict)

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
            'set_info': card_set_list
        }

        return card_dict

    @staticmethod
    def convert_cards_to_dicts(cards: List[Card]):
        # TODO documentation
        # TODO testing
        dict_card_list: List[dict] = []
        for card in cards:
            dict_card = DatabaseHandler.convert_card_to_dict(card)
            dict_card_list.append(dict_card)

        return dict_card_list

    @staticmethod
    def validate_database_connection():
        # TODO documentation
        # TODO testing
        result: bool = False
        mongo_client = MongoClient(CLIENT, serverselectiontimeoutms=TIMEOUT)
        try:
            mongo_client.server_info()
            logger.info("Successful connection to client.")
            result = True
        except errors.ServerSelectionTimeoutError as sste:
            logger.error(sste)
        finally:
            mongo_client.close()

        return result

    @staticmethod
    def count_number_records():
        # TODO documentation
        # TODO testing
        result: int = 0
        mongo_client = MongoClient(CLIENT, serverselectiontimeoutms=TIMEOUT)
        db = mongo_client[DATABASE]
        collection = db[COLLECTION]

        try:
            result = collection.count()
            logger.info('Number of records in database is ' + str(result))
        except errors.ServerSelectionTimeoutError as sste:
            logger.error(sste)
        finally:
            mongo_client.close()

        return result

    @staticmethod
    def persist_multiple_records_to_collection(records: List[dict]):
        # TODO documentation
        # TODO testing
        mongo_client = MongoClient(CLIENT, serverselectiontimeoutms=TIMEOUT)
        db = mongo_client[DATABASE]
        collection = db[COLLECTION]

        try:
            collection.insert_many(records)
            logger.info('Successfully inserted '+str(len(records))+' into database')
        except errors.ServerSelectionTimeoutError as sste:
            logger.error(sste)
        finally:
            mongo_client.close()

    @staticmethod
    def execute_query(query: dict):
        # TODO documentation
        # TODO testing
        cards: List[Card] = []
        mongo_client = MongoClient(CLIENT, serverselectiontimeoutms=TIMEOUT)
        db = mongo_client[DATABASE]
        collection = db[COLLECTION]

        try:
            cursor = collection.find(query)
            for card in cursor:
                cards.append(card)
        except errors.ServerSelectionTimeoutError as sste:
            logger.error(sste)
        finally:
            mongo_client.close()
        return cards

    @staticmethod
    def delete_all_records():
        # TODO documentation
        # TODO testing
        mongo_client = MongoClient(CLIENT, serverselectiontimeoutms=TIMEOUT)
        db = mongo_client[DATABASE]
        collection = db[COLLECTION]

        try:
            deleted = collection.delete_many({})
            logger.info('Number of records deleted: ' + str(deleted.deleted_count))
        except errors.ServerSelectionTimeoutError as sste:
            logger.error(sste)
        finally:
            mongo_client.close()