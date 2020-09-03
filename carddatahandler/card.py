from typing import List
from datetime import datetime


class SetInfo:

    def __init__(self, set_number: str = None, edition: str = None, rarity: str = None,
                 price: str = None, conditions: dict = None):
        if conditions is None:
            conditions = {'NM': 0,  # Near Mint: quantity
                          'LP': 0,  # Lightly Played: quantity
                          'MP': 0,  # Moderately Played: quantity
                          'HP': 0,  # Heavily Played: quantity
                          'D': 0}   # Damaged: quantity
        self._set_number = set_number
        self._edition = edition
        self._rarity = rarity
        self._price = price
        self._conditions = conditions

    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.__dict__ == other.__dict__:
            return True
        return False

    def set_set_number(self, set_number: str):
        self._set_number = set_number

    def set_edition(self, edition: str):
        self._edition = edition

    def set_rarity(self, rarity: str):
        self._rarity = rarity

    def set_price(self, price: str):
        self._price = price

    def set_conditions(self, condition: dict):
        self._conditions = condition

    def get_set_number(self):
        return self._set_number

    def get_edition(self):
        return self._edition

    def get_conditions(self):
        return self._conditions

    def get_rarity(self):
        return self._rarity

    def get_price(self):
        return self._price


class Card:

    def __init__(self, name: str = None, monster_type: str = None, attribute: str = None, race: str = None,
                 level: int = None, attack: int = None, defense: int = None, pass_code: int = None,
                 description: str = None, img_name: str = None, last_process_date: datetime = None, set_info: List[SetInfo] = None):
        self._name = name
        self._monster_type = monster_type
        self._attribute = attribute
        self._race = race
        self._level = level
        self._attack = attack
        self._defense = defense
        self._pass_code = pass_code
        self._description = description
        self._img_name = img_name
        self._last_process_date = last_process_date
        self._set_info = set_info if set_info is not None else []

    def __eq__(self, other):
        if self.__class__ == other.__class__ and self.__dict__ == other.__dict__:
            return True
        return False

    def set_name(self, name: str):
        self._name = name

    def set_monster_type(self, monster_type: str):
        self._monster_type = monster_type

    def set_attribute(self, attribute: str):
        self._attribute = attribute

    def set_race(self, race: str):
        self._race = race

    def set_level(self, level: int):
        self._level = level

    def set_attack(self, attack: int):
        self._attack = attack

    def set_defense(self, defense: int):
        self._defense = defense

    def set_pass_code(self, pass_code: int):
        self._pass_code = pass_code

    def set_description(self, description: str):
        self._description = description

    def set_set_info(self, set_info: List[SetInfo]):
        self._set_info = set_info

    def set_img_name(self, img_name: str):
        self._img_name = img_name

    def set_last_process_date(self, last_process_date: datetime):
        self._last_process_date = last_process_date

    def get_name(self):
        return self._name

    def get_monster_type(self):
        return self._monster_type

    def get_attribute(self):
        return self._attribute

    def get_race(self):
        return self._race

    def get_level(self):
        return self._level

    def get_attack(self):
        return self._attack

    def get_defense(self):
        return self._defense

    def get_pass_code(self):
        return self._pass_code

    def get_description(self):
        return self._description

    def get_img_name(self):
        return self._img_name

    def get_last_process_date(self):
        return self._last_process_date

    def get_set_info(self):
        return self._set_info

    # append set info method
    def append_set_info(self, new_set_info: SetInfo):
        self._set_info.append(new_set_info)
