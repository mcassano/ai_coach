import json
import os
from typing import Sequence

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
MOVEMENT_CONFIGURATION_FILE = '../movements.json'


class MovementExtractor:
    @staticmethod
    def get_movement(movement_name: str) -> dict:
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
    def read_movements(path: str) -> dict:
        with open(os.path.join(THIS_DIR, path)) as the_file:
            return json.load(the_file)

    @staticmethod
    def get_list_of_movements() -> Sequence[str]:
        return [mov['name']
                for mov in MovementExtractor.read_movements(
                MOVEMENT_CONFIGURATION_FILE)]
