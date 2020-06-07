from cardcollection.card import Card
import csv


# Data import from CSV with format of name,monster_type,attribute,level,attack,defense,edition,set_number,pass_code,condition,description
class DataImport:

    def __init__(self, file_location=None):
        self._file_location = file_location

    def init_indexes(self, header):
        iteration = 0
        name = None
        monster_type = None
        attribute = None
        level = None
        attack = None
        defense = None
        edition = None
        set_number = None
        pass_code = None
        condition = None
        description = None

        for column in header:
            if column == 'name':
                name = iteration
            elif column == 'monster_type':
                monster_type = iteration
            elif column == 'attribute':
                attribute = iteration
            elif column == 'level':
                level = iteration
            elif column == 'attack':
                attack = iteration
            elif column == 'defense':
                defense = iteration
            elif column == 'edition':
                edition = iteration
            elif column == 'set_number':
                set_number = iteration
            elif column == 'pass_code':
                pass_code = iteration
            elif column == 'condition':
                condition = iteration
            elif column == 'description':
                description = iteration
            iteration = iteration + 1

        return [name, monster_type, attribute, level, attack, defense, edition,
                set_number, pass_code, condition, description]

    def define_card_object(self, indexes, card_info):
        card_object = Card()
        if indexes[0] is not None:
            card_object.set_name(card_info[indexes[0]])
        elif indexes[1] is not None:
            card_object.set_monster_type(card_info[indexes[1]])
        elif indexes[2] is not None:
            card_object.set_attribute(card_info[indexes[2]])
        elif indexes[3] is not None:
            card_object.set_level(card_info[indexes[3]])
        elif indexes[4] is not None:
            card_object.set_attack(card_info[indexes[4]])
        elif indexes[5] is not None:
            card_object.set_defense(card_info[indexes[5]])
        elif indexes[6] is not None:
            card_object.set_edition(card_info[indexes[6]])
        elif indexes[7] is not None:
            card_object.set_set_number(card_info[indexes[7]])
        elif indexes[8] is not None:
            card_object.set_pass_code(card_info[indexes[8]])
        elif indexes[9] is not None:
            card_object.set_condition(card_info[indexes[9]])
        elif indexes[10] is not None:
            card_object.set_description(card_info[indexes[10]])
        return card_object

    def extract_data(self):
        card_list = []
        indexes = []

        # TODO Add config with datafile import location
        with open('C:/Users/ebyy2/PycharmProjects/CardCollection/data/Yugioh_Catalog_Monster_Full.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0

            for card_info in csv_reader:
                if line_count == 0:
                    indexes = self.init_indexes(card_info)
                elif indexes[0] is None:
                    # TODO throw and log error. Name must be specified for card
                    break
                elif all(val is None for val in indexes):
                    # TODO throw and log error. File format does not match expected format (name,monster_type,attribute,level,attack,defense,edition,set_number,pass_code,condition,description)
                    break
                else:
                    card_object = self.define_card_object(indexes, card_info)
                    card_list.append(card_object)
                line_count = line_count + 1
        pass
