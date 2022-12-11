import logging

import numpy as np
from src.annotation_result import AnnotationResult
from src.pose import PoseDetector
from src.pose_landmark import landmarks

logger = logging.getLogger(__name__)


class Annotator:
    def __init__(self, movement: dict, **kwargs):
        """
        :param movement:  Name from MovementExtractor
        :param kwargs:   Arguments passed to PoseDetector
        """
        self.recorded_count = 0
        self.direction = 0
        self.detector = PoseDetector(**kwargs)
        self.movement = movement
        # TODO: remove self.right_form.  It is transient.
        self.right_form = False
        self.prior_feedback = ''

    def annotate_frame(self, frame):
        # This was inspired from https://github.com/terminalai/PushUpCounter
        frame = self.detector.find_pose_and_draw_landmarks(frame, False)
        lm_list = self.detector.find_position(frame, False)
        all_points_in_frame = lm_list and all(
            lm_list[idx].in_frame
            for idx in (
                Annotator.landmark_indices_from_parts(
                    Annotator.parts_from_all_recipes(self.movement['angles'])))
        )
        # logger.debug(f'in_frame {all_points_in_frame} lm_list {lm_list}')
        logger.debug(f'in_frame {all_points_in_frame}')
        count = 0
        feedback = None
        per = None
        success = False
        angles = {}
        if lm_list:
            for angle in self.movement['angles']:
                # in the form of "LEFT_SHOULDER,LEFT_ELBOW,LEFT_WRIST"
                recipe_array = angle['recipe'].split(',')

                angles[angle['name']] = self.detector.find_and_draw_angle(
                    frame,
                    landmarks[recipe_array[0]],
                    landmarks[recipe_array[1]],
                    landmarks[recipe_array[2]])

            # Percentage of success of movement
            per = np.interp(
                angles[self.movement['steps'][0]['requirement'][0]['body']],
                (self.movement['steps'][1]['requirement'][0]['angle'],
                 self.movement['steps'][0]['requirement'][0]['angle']),
                (0, 100))

            logger.debug(f'angles: {angles}')

            # Check to ensure right form before starting the program
            # TODO: remove "self.right_form or"?
            # Why is that there?  That allows True even if the form is no
            # longer right
            self.right_form = (self.right_form
                               or (all_points_in_frame
                                   and Annotator.step_is_validated(
                                      self.movement['steps'][0]['requirement'],
                                      angles)
                                   ))

            # Check for full range of motion for the movement
            if not all_points_in_frame:
                feedback = 'Get In Frame'
            elif self.right_form:
                if per == 0:
                    step = self.movement['steps'][1]
                    next_step = self.movement['steps'][0]
                    if Annotator.step_is_validated(
                            step['requirement'],
                            angles):
                        feedback = next_step['name']
                        if self.direction == 0:
                            count = 0.5
                            self.direction = 1
                if per == 100:
                    step = self.movement['steps'][0]
                    next_step = self.movement['steps'][1]
                    if Annotator.step_is_validated(
                            step['requirement'],
                            angles):
                        feedback = next_step['name']
                        if self.direction == 1:
                            count = 0.5
                            self.direction = 0
            else:
                feedback = 'Fix Form'

            self.recorded_count = self.recorded_count + count
            success = True
        else:
            # Nothing was found, someone should get in the frame
            feedback = "Can't see your face"
            logger.debug('annotate frame found no pose ..')

        logger.debug(f'\'{feedback}\' \'{self.recorded_count}\'')
        # Store this for next frame, if the current frame does not
        # generate feedback then give the same feedback as the prior frame
        if feedback is None:
            feedback = self.prior_feedback

        # Store the current feedback because we might need it for next frame
        self.prior_feedback = feedback
        return AnnotationResult(frame,
                                feedback,
                                self.recorded_count,
                                per,
                                self.direction,
                                self.right_form,
                                success,
                                angles)

    @staticmethod
    def step_is_validated(requirements, angles):
        for key, value in angles.items():
            for requirement in requirements:
                if requirement['body'] == key:
                    if not Annotator.covert_requirement_to_predicate(
                            requirements,
                            key,
                            value):
                        return False
                else:
                    continue
        return True

    @staticmethod
    def covert_requirement_to_predicate(requirements, body_value, test_value):
        for requirement in requirements:
            body = requirement['body']
            test = requirement['test']
            angle = requirement['angle']
            if body == body_value:
                if test == 'gt':
                    return test_value > angle
                if test == 'gte':
                    return test_value >= angle
                if test == 'lt':
                    return test_value < angle
                if test == 'lte':
                    return test_value <= angle
        raise ValueError(f'{body_value} {test_value}')

    @staticmethod
    def parts_from_all_recipes(angles):
        parts = []
        for angle in angles:
            for name in angle['recipe'].split(','):
                parts.append(name)
        return list(set(parts))

    @staticmethod
    def landmark_indices_from_parts(parts):
        landmark_indices = []
        for part in parts:
            landmark_indices.append(landmarks[part])
        return landmark_indices
