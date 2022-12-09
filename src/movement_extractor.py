import json
from typing import Sequence

MOVEMENT_CONFIGURATION_FILE = './movements.json'


class MovementExtractor:
    @staticmethod
    def get_movement(movement_name: str):
        movements = MovementExtractor.read_movements(
                            MOVEMENT_CONFIGURATION_FILE)
        try:
            return next(
                mov for mov in movements if mov['name'] == movement_name)
        except StopIteration as err:
            raise ValueError(
                f"Movement '{movement_name}' not found in movements.json") \
                from err

    @staticmethod
    def read_movements(path: str):
        with open(path) as the_file:
            return json.load(the_file)

    @staticmethod
    def get_list_of_movements() -> Sequence[str]:
        return [mov['name']
                for mov in MovementExtractor.read_movements(
                MOVEMENT_CONFIGURATION_FILE)]
