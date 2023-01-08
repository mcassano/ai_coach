import json
import logging
import os
from typing import Sequence

import numpy as np
from src.pose_base import LandmarkLabel
from src.pose_landmark import landmarks

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
EXERCISE_CONFIGURATION_FILE = '../exercises.json'
logger = logging.getLogger(__name__)


class Angle:
    def __init__(self, name: str, recipe: str):
        self.name = name
        # recipe is in the form of "LEFT_SHOULDER,LEFT_ELBOW,LEFT_WRIST"
        self.landmark_indexes = [
            landmarks[name] for name in recipe.split(',')]
        assert len(self.landmark_indexes) == 3

    def __str__(self):
        return f'Angle {self.name} landmarks {self.landmark_indexes}'


class Requirement:
    def __init__(self, definition: dict, all_angles: dict[str, Angle]):
        # NOTE: 'body_angle' refers to an angle defined in all_angles.
        self.body_angle = all_angles[definition['body_angle']]
        self._test = definition['test']
        self.angle = definition['angle']
        self._test_near_degrees = definition.get('near_degrees', None)

    def test_req(self, body_value, test_value):
        if self._test == 'gt':
            return test_value > self.angle
        if self._test == 'gte':
            return test_value >= self.angle
        if self._test == 'lt':
            return test_value < self.angle
        if self._test == 'lte':
            return test_value <= self.angle
        if self._test == 'near':
            return abs(test_value - self.angle) <= self._test_near_degrees

        raise ValueError(
            f'Unknown test {self._test}, {body_value} {test_value}')

    def __str__(self):
        return f'{self.body_angle} {self._test} {self.angle}'


class Pose:
    def __init__(self, name: str, requirements: list[dict],
                 all_angles: dict[str, Angle]):
        self.name = name
        self.requirements = [Requirement(defn, all_angles)
                             for defn in requirements]

    def body_angles(self):
        return {req.body_angle for req in self.requirements}

    def validation_result(self, angles: dict[str, float]) -> dict[str, bool]:
        """Dict with whether each pose angle is valid."""
        match_result = {}
        for angle_name, angle_value in angles.items():
            logger.debug(f'angle {angle_name} value {angle_value}')
            for requirement in self.requirements:
                if requirement.body_angle.name == angle_name:
                    logger.debug(
                        f'test req {requirement} with'
                        f' angle {angle_name} {angle_value}')
                    match_result[angle_name] = requirement.test_req(
                        requirement.angle, angle_value)
                else:
                    continue

        # should have tested all requirements
        assert len(match_result) == len(self.requirements), match_result
        return match_result

    def is_validated(self, angles: dict[str, float]):
        """Return True if all pose angles are valid"""
        return all(self.validation_result(angles).values())


class Step:
    def __init__(self, definition: dict, all_poses: dict[str, Pose]):
        self.name = definition['name']
        # Number of seconds to hold the pose
        self.default_target_seconds = definition.get(
            'default_target_seconds', None)
        # NOTE: audio is not currently used
        # self.audio = definition['audio']
        self.pose = all_poses[definition['pose']]


class Exercise:
    def __init__(self, name: str,
                 all_poses: dict[str, Pose],
                 definition: dict[str, dict]):
        self.name = name
        self.default_target_reps = definition['default_target_reps']
        self.steps = [Step(step, all_poses) for step in definition['steps']]
        # What if multiple steps have default_target_seconds?  Is that a thing?
        self.default_target_seconds = self.steps[0].default_target_seconds

        # all angles in all steps
        self.angles = [angle
                       for step in self.steps
                       for angle in step.pose.body_angles()]
        self._indexes_from_angles = self._landmark_indexes_from_all_angles(
            self.angles)

    # TODO: Unit test percentage
    def percentage(self, angles: dict[str, float]):
        # arbitrarily pick req 0 to measure percentage on
        first_step_req = self.steps[0].pose.requirements[0]
        next_step_req = self.steps[1].pose.requirements[0]
        # has to be the same body part angle
        assert first_step_req.body_angle == next_step_req.body_angle

        return np.interp(
            angles[first_step_req.body_angle.name],
            (next_step_req.angle, first_step_req.angle),
            (0, 100))

    def all_points_in_frame(self, lm_list: list[LandmarkLabel]):
        return lm_list and all(
            lm_list[idx].in_frame
            for idx in self._indexes_from_angles)

    def first_step_validated(self, angles):
        return self.steps[0].pose.is_validated(angles)

    @staticmethod
    def _landmark_indexes_from_all_angles(angles: Sequence[Angle]):
        idxs = set()
        for angle in angles:
            idxs |= set(angle.landmark_indexes)
        # why list(set(..))?
        return list(set(idxs))

    @staticmethod
    def exercise(exercise_name: str) -> 'Exercise':
        exercises = Exercise._read_exercises(EXERCISE_CONFIGURATION_FILE)
        # Raises KeyError if exercise_name is unknown
        return exercises[exercise_name]

    @staticmethod
    def _read_exercises(path: str) -> dict[str, 'Exercise']:
        # Read file, return all Movement objects
        with open(os.path.join(THIS_DIR, path)) as the_file:
            data = json.load(the_file)
            all_angles = {name: Angle(name, recipe)
                          for name, recipe in data['angles'].items()}
            all_poses = {name: Pose(name, requirements, all_angles)
                         for name, requirements in data['poses'].items()}
            return {key: Exercise(key, all_poses, val)
                    for key, val in data['exercises'].items()}

    @staticmethod
    def exercise_names() -> Sequence[str]:
        return list(Exercise._read_exercises(
            EXERCISE_CONFIGURATION_FILE).keys())
