import logging
import time
from typing import Optional

from src.advice_steps import AdviceSteps
from src.annotation_result import AnnotationResult
from src.exercise import Exercise
from src.pose import PoseDetector

logger = logging.getLogger(__name__)


class Annotator:
    def __init__(self, exercise: Exercise, target_seconds: Optional[int], **kwargs):
        """
        :param exercise:  Exercise
        :param target_seconds:  Number of seconds to hold an exercise
        :param kwargs:   Arguments passed to PoseDetector
        """
        self.recorded_count = 0
        self.direction = 0
        self.detector = PoseDetector(**kwargs)
        self.exercise = exercise
        # TODO: remove self.right_form.  It is transient.
        self.right_form = False
        self.right_form_start: Optional[float] = None
        self.right_form_seconds: Optional[int] = None
        self.prior_feedback = ""
        self.target_seconds = target_seconds

    def annotate_frame(self, frame) -> AnnotationResult:
        # This was inspired from https://github.com/terminalai/PushUpCounter
        frame = self.detector.find_pose_and_draw_landmarks(frame, False)
        lm_list = self.detector.find_position(frame, False)
        all_points_in_frame = self.exercise.all_points_in_frame(lm_list)
        # logger.debug(f'in_frame {all_points_in_frame} lm_list {lm_list}')
        logger.debug(f"in_frame {all_points_in_frame}")
        count = 0
        rep_completed = False
        seconds_left = None
        feedback = None
        per = None
        success = False
        angles = {}
        angle_validation = {}

        num_steps = len(self.exercise.steps)
        logger.debug(f"num_steps {num_steps}")
        assert 1 <= num_steps <= 2, "We only handle one or two step exercises"

        if lm_list:
            for angle in self.exercise.angles:
                angles[angle.name] = self.detector.find_and_draw_angle(
                    frame, *angle.landmark_indexes
                )

            logger.debug(f"angles: {angles}")

            # Check to ensure right form before starting the program
            # TODO: remove "self.right_form or"
            # NOTE: currently, right_form is sticky, but that is not great
            # What if we get out of form?
            # We should say "Fix Form" but the stickiness will prevent it.
            self.right_form = self.right_form or (
                all_points_in_frame and self.exercise.first_step_validated(angles)
            )
            if self.right_form:
                if not self.right_form_start:
                    self.right_form_start = time.time()
                self.right_form_seconds = int(time.time() - self.right_form_start)

            # Percentage of success of exercise, and which step we're on
            if num_steps == 2:
                per = self.exercise.percentage(angles)
            else:
                assert num_steps == 1
                per = 100
            current_step_idx = 0
            if num_steps == 2 and per == 0:
                current_step_idx = 1

            # Validate step
            if not all_points_in_frame:
                feedback = AdviceSteps.GET_IN_FRAME.value.title
            elif self.right_form:
                # Check the current step of the exercise
                count, feedback, rep_completed, seconds_left = self._examine_step(
                    num_steps, current_step_idx, angles
                )
            else:
                feedback = "Fix Form"
                angle_validation = self.exercise.steps[
                    current_step_idx
                ].pose.validation_result(angles)

            self.recorded_count = self.recorded_count + count
            success = True
        else:
            # Nothing was found, someone should get in the frame
            # TODO: Play audio for this
            feedback = "Can't see your face"
            logger.debug("annotate frame found no pose ..")

        logger.debug(f"'{feedback}' '{self.recorded_count}'")
        # Store this for next frame, if the current frame does not
        # generate feedback then give the same feedback as the prior frame
        if feedback is None:
            feedback = self.prior_feedback
            logger.debug("feedback is None, use prior_feedback")

        logger.debug("===============")

        # Store the current feedback because we might need it for next frame
        self.prior_feedback = feedback
        return AnnotationResult(
            frame,
            feedback,
            self.recorded_count,
            rep_completed,
            per,
            self.direction,
            self.right_form,
            self.right_form_seconds,
            seconds_left,
            angle_validation,
            success,
            angles,
            num_steps,
        )

    def _examine_step(self, num_steps: int, current_step_idx: int, angles):
        count = 0.0
        rep_completed = False
        feedback = None
        current_step = self.exercise.steps[current_step_idx]
        seconds_left = None

        if num_steps == 2:
            if current_step_idx == 1:
                next_step = self.exercise.steps[0]
                if current_step.pose.is_validated(angles):
                    feedback = next_step.name
                    if self.direction == 0:
                        count = 0.5
                        self.direction = 1
            elif current_step_idx == 0:
                next_step = self.exercise.steps[1]
                if current_step.pose.is_validated(angles):
                    feedback = next_step.name
                    if self.direction == 1:
                        count = 0.5
                        rep_completed = True
                        self.direction = 0
        else:
            assert num_steps == 1
            assert self.target_seconds is not None and self.target_seconds > 0
            assert self.right_form_seconds is not None

            if self.right_form_seconds >= self.target_seconds:
                # TODO: fix bug here that counts reps rapidly, since
                #   we remain done
                rep_completed = True
                count = 1
                feedback = "Done"
            else:
                seconds_left = self.target_seconds - self.right_form_seconds
                feedback = "Hold"

        return count, feedback, rep_completed, seconds_left
