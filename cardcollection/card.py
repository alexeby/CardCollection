class Card:

    def __init__(self, name=None, monster_type=None, attribute=None, level=None, attack=None, defense=None, edition=None,
                 set_number=None, pass_code=None, condition=None, description=None, img_name=None, quantity=0, last_process_date=None):
        self._name = name
        self._monster_type = monster_type
        self._attribute = attribute
        self._level = level
        self._attack = attack
        self._defense = defense
        self._edition = edition
        self._set_number = set_number
        self._pass_code = pass_code
        self._condition = condition
        self._description = description
        self._img_name = img_name
        self._quantity = quantity
        self._last_process_date = last_process_date

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

    def set_edition(self, edition):
        self._edition = edition

    def set_set_number(self, set_number):
        self._set_number = set_number

    def set_pass_code(self, pass_code):
        self._pass_code = pass_code

    def set_condition(self, condition):
        self._condition = condition

    def set_description(self, description):
        self._description = description

    def set_img_name(self, img_name):
        self._img_name = img_name

    def set_quantity(self, quantity):
        self._quantity = quantity

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

    def get_edition(self):
        return self._edition

    def get_set_number(self):
        return self._set_number

    def get_pass_code(self):
        return self._pass_code

    def get_condition(self):
        return self._condition

    def get_description(self):
        return self._description

    def get_img_name(self):
        return self._img_name

    def get_quantity(self):
        return self._quantity

    def get_last_process_date(self):
        return self._last_process_date
