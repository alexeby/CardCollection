class SetInfo:

    def __init__(self, set_number=None, edition=None, rarity=None, price=None, conditions=None):
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

    def set_set_number(self, set_number):
        self._set_number = set_number

    def set_edition(self, edition):
        self._edition = edition

    def set_rarity(self, rarity):
        self._rarity = rarity

    def set_price(self, price):
        self._price = price

    def set_conditions(self, condition):
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

    def __init__(self, name=None, monster_type=None, attribute=None, level=None, attack=None, defense=None,
                 pass_code=None, description=None, img_name=None, last_process_date=None, set_info=None):
        self._name = name
        self._monster_type = monster_type
        self._attribute = attribute
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

    def set_name(self, name):
        self._name = name

    def set_monster_type(self, monster_type):
        self._monster_type = monster_type

    def set_attribute(self, attribute):
        self._attribute = attribute

    def set_level(self, level):
        self._level = level

    def set_attack(self, attack):
        self._attack = attack

    def set_defense(self, defense):
        self._defense = defense

    def set_pass_code(self, pass_code):
        self._pass_code = pass_code

    def set_description(self, description):
        self._description = description

    def set_img_name(self, img_name):
        self._img_name = img_name

    def set_last_process_date(self, last_process_date):
        self._last_process_date = last_process_date

    def get_name(self):
        return self._name

    def get_monster_type(self):
        return self._monster_type

    def get_attribute(self):
        return self._attribute

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

    def set_set_info(self, set_info):
        self._set_info = set_info

    def get_set_info(self):
        return self._set_info

    # append set info method
    def append_set_info(self, new_set_info: SetInfo):
        self._set_info.append(new_set_info)
