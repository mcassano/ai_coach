import logging
import time

from src.annotation_result import AnnotationResult
from src.exercise import Exercise
from src.pose import PoseDetector

logger = logging.getLogger(__name__)


class Annotator:
    def __init__(self, exercise: Exercise, **kwargs):
        """
        :param exercise:  Exercise
        :param kwargs:   Arguments passed to PoseDetector
        """
        self.recorded_count = 0
        self.direction = 0
        self.detector = PoseDetector(**kwargs)
        self.exercise = exercise
        # TODO: remove self.right_form.  It is transient.
        self.right_form = False
        self.right_form_start = None
        self.right_form_seconds = None
        self.prior_feedback = ''

    # TODO: Unit test annotate_frame
    def annotate_frame(self, frame):
        # This was inspired from https://github.com/terminalai/PushUpCounter
        frame = self.detector.find_pose_and_draw_landmarks(frame, False)
        lm_list = self.detector.find_position(frame, False)
        all_points_in_frame = self.exercise.all_points_in_frame(lm_list)
        # logger.debug(f'in_frame {all_points_in_frame} lm_list {lm_list}')
        logger.debug(f'in_frame {all_points_in_frame}')
        count = 0
        rep_completed = False
        feedback = None
        per = None
        success = False
        angles = {}

        assert 1 <= len(self.exercise.steps) <= 2, (
            'We only handle one or two step exercises')
        two_step = 2 == len(self.exercise.steps)
        one_step = 1 == len(self.exercise.steps)

        if lm_list:
            for angle in self.exercise.angles:
                angles[angle.name] = self.detector.find_and_draw_angle(
                    frame, *angle.landmark_indexes)

            # Percentage of success of exercise
            if two_step:
                per = self.exercise.percentage(angles)
            else:
                assert one_step
                per = 100

            logger.debug(f'angles: {angles}')

            # Check to ensure right form before starting the program
            # TODO: remove "self.right_form or"?
            # NOTE: currently, right_form is sticky, but that feels weird
            self.right_form = (
                    self.right_form
                    or (all_points_in_frame
                        and self.exercise.first_step_validated(angles)))
            if self.right_form:
                if not self.right_form_start:
                    self.right_form_start = time.time()
                self.right_form_seconds = int(
                    time.time() - self.right_form_start)

            # Check for full range of motion for the exercise
            if not all_points_in_frame:
                feedback = 'Get In Frame'
            elif self.right_form:
                if two_step:
                    count, feedback, rep_completed = self.two_step_count(
                        angles, count, feedback, per, rep_completed)
                else:
                    assert one_step
                    count, rep_completed = self.one_step_count(
                        count, rep_completed)
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
            logger.debug('feedback is None, use prior_feedback')

        # Store the current feedback because we might need it for next frame
        self.prior_feedback = feedback
        return AnnotationResult(frame,
                                feedback,
                                self.recorded_count,
                                rep_completed,
                                per,
                                self.direction,
                                self.right_form,
                                self.right_form_seconds,
                                success,
                                angles)

    def one_step_count(self, count, rep_completed):
        the_step = self.exercise.steps[0]
        assert the_step.target_seconds > 0
        if self.right_form_seconds >= the_step.target_seconds:
            rep_completed = True
            count = 1
        return count, rep_completed

    def two_step_count(self, angles, count, feedback, per, rep_completed):
        if per == 0:
            step = self.exercise.steps[1]
            next_step = self.exercise.steps[0]
            if step.pose.is_validated(angles):
                feedback = next_step.name
                if self.direction == 0:
                    count = 0.5
                    self.direction = 1
        if per == 100:
            step = self.exercise.steps[0]
            next_step = self.exercise.steps[1]
            if step.pose.is_validated(angles):
                feedback = next_step.name
                if self.direction == 1:
                    count = 0.5
                    rep_completed = True
                    self.direction = 0
        return count, feedback, rep_completed
