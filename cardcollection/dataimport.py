import csv
import logging

from cardcollection.card import *
from typing import List

logger = logging.getLogger(__name__)


# Data import from CSV with format of name,monster_type,attribute,level,attack,defense,edition,set_number,pass_code,condition,description
class DataImport:

    def __init__(self, file_location=None):
        self._file_location = file_location

    @staticmethod
    def init_indexes(header):
        iteration = 0
        index_dict = {'name': None,
                      'monster_type': None,
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
            elif column == 'monster_type': index_dict['monster_type'] = iteration
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
            iteration = iteration + 1

        return index_dict

    def define_card_object(self, indexes: dict, card_info: list):
        card_object = Card()

        # Align card object information
        if indexes['name'] is not None: card_object.set_name(card_info[indexes['name']])
        if indexes['monster_type'] is not None: card_object.set_monster_type(card_info[indexes['monster_type']])
        if indexes['attribute'] is not None: card_object.set_attribute(card_info[indexes['attribute']])
        if indexes['level'] is not None: card_object.set_level(card_info[indexes['level']])
        if indexes['attack'] is not None: card_object.set_attack(card_info[indexes['attack']])
        if indexes['defense'] is not None: card_object.set_defense(card_info[indexes['defense']])
        if indexes['pass_code'] is not None: card_object.set_pass_code(card_info[indexes['pass_code']])
        if indexes['description'] is not None: card_object.set_description(card_info[indexes['description']])

        # Align card set info with card object. There can be more than one card set per card object
        set_info = SetInfo()
        if indexes['set_number'] is not None: set_info.set_set_number(card_info[indexes['set_number']])
        if indexes['edition'] is not None: set_info.set_edition(card_info[indexes['edition']])
        if indexes['condition'] is not None: set_info.set_condition(card_info[indexes['condition']])
        card_object.append_set_info(set_info)

        return card_object

    def index_of_existing_data(self, new_card: Card, card_list: List[Card]):
        index = 0
        for existing_card in card_list:
            if new_card.get_name() == existing_card.get_name():
                return index
            index = index + 1

        return None


    def categorize_data(self, csv_reader):
        card_list = []
        indexes = []
        line_count = 0

        for card_info in csv_reader:
            if line_count == 0:
                indexes = self.init_indexes(card_info)
            # TODO throw and log error. Name must be specified for card
            # TODO throw and log error. File format does not match expected format (name,monster_type,attribute,level,attack,defense,edition,set_number,pass_code,condition,description)
            else:
                card_object = self.define_card_object(indexes, card_info)
                index_of_existing = self.index_of_existing_data(card_object, card_list)
                if index_of_existing is None:
                    card_list.append(card_object)
                else:
                    # TODO don't add duplicate sets
                    existing_card_object = card_list[index_of_existing]
                    existing_card_object.append_set_info(card_object.get_set_info()[0]) # TODO potential error check here
                    card_list[index_of_existing] = existing_card_object
            line_count = line_count + 1

        return card_list

    def extract_csv_data(self):
        # TODO Add config with datafile import location
        with open('C:/Users/ebyy2/PycharmProjects/CardCollection/data/Yugioh_Catalog_Monster_Full.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.categorize_data(csv_reader)
