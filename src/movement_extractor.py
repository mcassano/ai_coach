import json

MOVEMENT_CONFIGURATION_FILE = './movements.json'


class MovementExtractor:
    @staticmethod
    def get_movement(movement_name):
        movements = MovementExtractor.read_movements(
                            MOVEMENT_CONFIGURATION_FILE)

        movement = None
        for each_movement in movements:
            if each_movement['name'] == movement_name:
                movement = each_movement
                break

        if movement is None:
            raise ValueError(
                "Movement '%s' not found in movements.json" % movement_name)

        return movement

    @staticmethod
    def read_movements(path):
        with open(path) as the_file:
            movements = json.load(the_file)
        return movements

    @staticmethod
    def get_list_of_movements():
        movements = MovementExtractor.read_movements(
                            MOVEMENT_CONFIGURATION_FILE)
        movement_names = []
        for movement in movements:
            movement_names.append(movement['name'])
        return movement_names
