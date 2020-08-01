import csv
import logging
from cardcollectionsyncronizer.card import Card, SetInfo
from typing import List

logger = logging.getLogger(__name__)


class DataImport:
    """Used to import data from csv file. CSV columns should be any of the following values: name, race_type,
    attribute, level, attack, defense, edition, set_number, pass_code, condition, description. The order of these
    columns is not a concern as they will be automatically indexed and put in a dictionary.
    """

    def __init__(self, file_location=None):
        self._file_location = file_location

    @staticmethod
    def init_indexes(header):
        """Initializes the indexes of the import file based on the headers of columns.

        :param header: the header row of the import file.
        :type header: list
        :return: dictionary of indexes for the data within the import file.
        :rtype: dict
        """
        iteration = 0
        index_dict = {'name': None,
                      'race_type': None,
                      'attribute': None,
                      'level': None,
                      'attack': None,
                      'defense': None,
                      'pass_code': None,
                      'description': None,
                      'set_number': None,
                      'edition': None,
                      'rarity': None,
                      'condition': None}

        for column in header:
            if column == 'name': index_dict['name'] = iteration
            elif column == 'race_type': index_dict['race_type'] = iteration
            elif column == 'attribute': index_dict['attribute'] = iteration
            elif column == 'level': index_dict['level'] = iteration
            elif column == 'attack': index_dict['attack'] = iteration
            elif column == 'defense': index_dict['defense'] = iteration
            elif column == 'pass_code': index_dict['pass_code'] = iteration
            elif column == 'description': index_dict['description'] = iteration
            elif column == 'set_number': index_dict['set_number'] = iteration
            elif column == 'edition': index_dict['edition'] = iteration
            elif column == 'rarity': index_dict['rarity'] = iteration
            elif column == 'condition': index_dict['condition'] = iteration
            else:
                logger.warning(column + ' is not an expected attribute for card import data')
            iteration = iteration + 1

        return index_dict

    @staticmethod
    def get_monster_race_and_type(race_type: str):
        race_type_list: List[str] = race_type.split('/')
        result: dict = {'race': None, 'monster_type': None}
        i = 0
        for rt in race_type_list:
            rt = rt.strip()
            if i == 0:
                result['race'] = rt
            else:
                result['monster_type'] = rt if result['monster_type'] is None else result['monster_type'] + ' ' + rt
            i += 1

        if result['monster_type'] is None:
            result['monster_type'] = 'Normal Monster'
        else:
            result['monster_type'] += ' Monster'
        return result

    @staticmethod
    def define_card_object(indexes: dict, card_info: list):
        """Creates card object and sets card attributes from imported information.

        :param indexes: indexes of imported data
        :type indexes: dict
        :param card_info: imported card data in list format
        :type card_info: list
        :return: newly created card object
        :rtype: Card
        """
        card_object = Card()

        # Align card object information
        if indexes['name'] is not None: card_object.set_name(card_info[indexes['name']])
        if indexes['attribute'] is not None: card_object.set_attribute(card_info[indexes['attribute']])
        if indexes['level'] is not None: card_object.set_level(int(card_info[indexes['level']]))
        if indexes['attack'] is not None: card_object.set_attack(int(card_info[indexes['attack']]))
        if indexes['defense'] is not None: card_object.set_defense(int(card_info[indexes['defense']]))
        if indexes['pass_code'] is not None: card_object.set_pass_code(card_info[indexes['pass_code']])
        if indexes['description'] is not None: card_object.set_description(card_info[indexes['description']])
        if indexes['race_type'] is not None:
            race_types: dict = DataImport.get_monster_race_and_type(card_info[indexes['race_type']])
            card_object.set_race(race_types.get('race'))
            card_object.set_monster_type(race_types.get('monster_type'))

        # Align card set info with card object. There can be more than one card set per card object
        set_info = SetInfo()
        if indexes['set_number'] is not None: set_info.set_set_number(card_info[indexes['set_number']])
        if indexes['edition'] is not None: set_info.set_edition(card_info[indexes['edition']])

        # Conditions are handled a bit differently. They are stored in dictionary and are used to determine quantity
        new_condition = card_info[indexes['condition']]
        conditions = DataImport.handle_conditions(set_info.get_conditions(), new_condition)
        if indexes['condition'] is not None: set_info.set_conditions(conditions)

        card_object.append_set_info(set_info)
        return card_object

    @staticmethod
    def get_key_from_value(d: dict, v):
        """Gets the key from the value of dictionary.

        :param d: dictionary to retrieve key from value
        :type d: dict
        :param v: value to use to retrieve key
        :return: key of the passed value
        :rtype: type of key in dictionary
        """
        for key, value in d.items():
            if value == v:
                return key

    @staticmethod
    def index_of_existing_data(new_card: Card, card_list: List[Card]):
        """Searches for existing cards that may have already been imported. This eliminates the possibility of
        duplicate cards being imported.

        :param new_card: card being imported
        :type new_card: Card
        :param card_list: existing cards already imported
        :type card_list: List[Card]
        :return: index of existing card. If their are none, returns None
        :rtype: int
        """
        index = 0
        for existing_card in card_list:
            if new_card.get_name() == existing_card.get_name():
                return index
            index = index + 1

    @staticmethod
    def handle_conditions(existing_conditions: dict, new_condition: str):
        """For cards of the same set that have already been imported, increases the number of that importing condition
        by 1.

        :param existing_conditions: dictionary of the existing condition for that set
        :type existing_conditions: dict
        :param new_condition: condition to have 1 added to
        :type new_condition: str
        :return: the updated conditions for that set
        :rtype: dict
        """
        try:
            existing_conditions[new_condition] = existing_conditions[new_condition] + 1
        except KeyError:
            logger.error(KeyError)

        return existing_conditions

    @staticmethod
    def do_sets_match(set1: SetInfo, set2: SetInfo):
        """Verifies if the sets of 2 of the same cards match. This is based on the cards set number and edition.

        :param set1: set1
        :type set1: SetInfo
        :param set2: set2
        :type set2: SetInfo
        :return: returns True if card sets match, else returns false.
        :rtype: bool
        """
        match = False
        if set1.get_set_number() == set2.get_set_number() \
                and set1.get_edition() == set2.get_edition():
            match = True

        return match

    @staticmethod
    def handle_set_info(new_card: Card, existing_card: Card):
        """For matching cards, merges the set data from the newly imported card to that of the existing card. If the
        sets do not match, a new set will be added to the card object. If the sets do match, the sets conditions will
        be merged.

        :param new_card: the card being imported
        :param existing_card: the card that has already been imported
        :return: updated card with adjusted set data
        :rtype: Card
        """
        new_card_set = SetInfo()
        try:
            new_card_set = new_card.get_set_info()[0]
        except IndexError:
            logger.error('Error occurred with card: ' + new_card.get_name(), IndexError)

        if new_card_set == SetInfo():
            return None

        no_match_found = True
        existing_sets = existing_card.get_set_info()
        existing_set: SetInfo
        for existing_set in existing_sets:
            if DataImport.do_sets_match(existing_set, new_card_set):
                no_match_found = False
                new_condition: str = DataImport.get_key_from_value(new_card_set.get_conditions(), 1)
                updated_conditions = DataImport.handle_conditions(existing_set.get_conditions(), new_condition)
                existing_set.set_conditions(updated_conditions)
                break

        if no_match_found:
            existing_sets.append(new_card_set)

        existing_card.set_set_info(existing_sets)
        return existing_card

    def categorize_data(self, csv_reader):
        """Organizes the CSV data by initializing the header indexes, verifying that card has necessary information to
        be imported, and driving the handling of set data for matching cards.

        :param csv_reader: reader (rows) of CSV file containing card data
        :type csv_reader: _reader
        :return: imported card data
        :rtype: List[Card]
        """
        card_list: list = []
        indexes: dict = {}
        line_count: int = 0

        for card_info in csv_reader:
            if line_count == 0:
                indexes = self.init_indexes(card_info)
            elif card_info['name'] is None:
                logger.error('Name must be specified for card')
            else:
                card_object = self.define_card_object(indexes, card_info)
                index_of_existing = self.index_of_existing_data(card_object, card_list)
                if index_of_existing is None:
                    card_list.append(card_object)
                else:
                    existing_card_object = card_list[index_of_existing]
                    try:
                        # Don't add duplicate sets
                        existing_card_object = self.handle_set_info(card_object, existing_card_object)
                        card_list[index_of_existing] = existing_card_object
                    except IndexError:
                        logger.error('Error occurred with card: ' + card_object.get_name(), IndexError)

            line_count = line_count + 1

        return card_list

    def extract_csv_data(self):
        """Loads the CSV file with card information to be imported.

        :return: imported card data
        :rtype: List[Card]
        """
        with open(self._file_location, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            return self.categorize_data(csv_reader)
