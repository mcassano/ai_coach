import json
import os
from typing import Sequence

import numpy as np
from src.pose_base import LandmarkLabel
from src.pose_landmark import landmarks

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
MOVEMENT_CONFIGURATION_FILE = '../movements.json'


class Angle:
    def __init__(self, definition: dict):
        self.name = definition['name']
        # recipe is in the form of "LEFT_SHOULDER,LEFT_ELBOW,LEFT_WRIST"
        self.landmark_indexes = [
            landmarks[name] for name in definition['recipe'].split(',')]
        assert len(self.landmark_indexes) == 3


class Requirement:
    def __init__(self, definition):
        self.body = definition['body']
        self._test = definition['test']
        self.angle = definition['angle']

    def test_req(self, body_value, test_value):
        if self._test == 'gt':
            return test_value > self.angle
        if self._test == 'gte':
            return test_value >= self.angle
        if self._test == 'lt':
            return test_value < self.angle
        if self._test == 'lte':
            return test_value <= self.angle

        raise ValueError(f'{body_value} {test_value}')


class Step:
    def __init__(self, definition):
        self.name = definition['name']
        self.requirements = [
            Requirement(defn) for defn in definition['requirement']]

    def is_validated(self, angles: dict[str, float]):
        for angle_name, angle_value in angles.items():
            for requirement in self.requirements:
                if requirement.body == angle_name:
                    if not requirement.test_req(
                            requirement.angle, angle_value):
                        return False
                else:
                    continue
        return True


# TODO: Rename to 'Exercise'?
class Movement:
    def __init__(self, definition: dict):
        self.name = definition['name']
        self.angles = [Angle(defn) for defn in definition['angles']]
        self.steps = [Step(defn) for defn in definition['steps']]
        self._indexes_from_angles = self._landmark_indexes_from_all_angles(
            self.angles)

    def percentage(self, angles: dict[str, float]):
        # arbitrarily pick req 0 to measure percentage on
        first_step_req = self.steps[0].requirements[0]
        next_step_req = self.steps[1].requirements[0]
        # has to be the same body part angle
        assert first_step_req.body == next_step_req.body

        return np.interp(
            angles[first_step_req.body],
            (next_step_req.angle, first_step_req.angle),
            (0, 100))

    def all_points_in_frame(self, lm_list: list[LandmarkLabel]):
        return lm_list and all(
            lm_list[idx].in_frame
            for idx in self._indexes_from_angles)

    def all_steps_validated(self, angles):
        return all(step.is_validated(angles) for step in self.steps)

    @staticmethod
    def _landmark_indexes_from_all_angles(angles):
        idxs = set()
        for angle in angles:
            idxs |= set(angle.landmark_indexes)
        # why list(set(..))?
        return list(set(idxs))

    @staticmethod
    def get_movement(movement_name: str) -> 'Movement':
        movements = Movement._read_movements(
                            MOVEMENT_CONFIGURATION_FILE)
        try:
            return next(
                Movement(mov)
                for mov in movements if mov['name'] == movement_name)
        except StopIteration as err:
            raise ValueError(
                f"Movement '{movement_name}' not found in movements.json") \
                from err

    @staticmethod
    def _read_movements(path: str) -> dict:
        with open(os.path.join(THIS_DIR, path)) as the_file:
            return json.load(the_file)

    @staticmethod
    def get_list_of_movements() -> Sequence[str]:
        return [Movement(mov).name
                for mov in Movement._read_movements(
                    MOVEMENT_CONFIGURATION_FILE)]
