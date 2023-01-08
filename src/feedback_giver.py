import logging
import time
from typing import Optional

from src.advice_steps import AdviceSteps
from src.audio import generate_audio_file, play_audio_file

logger = logging.getLogger(__name__)


class FeedbackGiver:
    """Give audio feedback when appropriate."""

    def __init__(self):
        self._last_audio_time = 0

    def _play_audio_file(self, path: str):
        play_audio_file(path)
        self._last_audio_time = time.time()

    def _play_advice_step(self, step: AdviceSteps):
        self._play_audio_file(step.value.audio_path)

    def _play_count(self, count):
        """Generate and play an integer count"""
        # make sure count isn't a decimal: 1.0 --> 1
        self._play_text(str(int(count)))

    def _play_text(self, text):
        """Generate and play any text passed"""
        fullpath = generate_audio_file(text)
        self._play_audio_file(fullpath)

    def give_feedback(
            self,
            exercise_num_steps: int,
            count: float, rep_completed: bool,
            target_reps: int,
            right_form_seconds: Optional[int],
            feedback: str, prior_feedback: str,
            angle_validation: dict[str, bool]):
        """Give feedback if applicable (i.e. not too often)"""
        logger.debug(
            f'count {count} target_reps {target_reps}'
            f' feedback "{feedback}" prior_feedback "{prior_feedback}"'
            f' right_form_seconds {right_form_seconds}'
            f' exercise_num_steps {exercise_num_steps}')
        seconds_since_audio = time.time() - self._last_audio_time

        # If the count changed, play the new one
        if rep_completed and exercise_num_steps == 2:
            if count == target_reps:
                self._play_advice_step(AdviceSteps.DONE)
            # Give specific count
            elif count > 0:
                self._play_count(count)
            else:
                self._play_advice_step(AdviceSteps.GOOD)
        elif exercise_num_steps == 1 and right_form_seconds:
            # This is a one-step exercise we hold
            # Let's count the seconds
            # TODO: how to not skip counting some seconds?
            # "seconds_since_audio" >= 1 above is not cutting it
            if feedback != 'Done':
                if seconds_since_audio >= 1:
                    self._play_count(right_form_seconds)
            elif feedback == 'Done' and prior_feedback != 'Done':
                assert rep_completed
                self._play_advice_step(AdviceSteps.DONE)
        # Get in Frame but only after some seconds
        elif (feedback == AdviceSteps.GET_IN_FRAME.value.title
                and seconds_since_audio > 2):
            self._play_advice_step(AdviceSteps.GET_IN_FRAME)
        # Fix form but only after some seconds
        elif (feedback == AdviceSteps.FIX_FORM.value.title
              and seconds_since_audio > 2):
            # say how to fix the form by mentioning the first bad angle
            logger.warning(f'Angle validation: {angle_validation}')
            bad_angles = [key for key in angle_validation
                          if not angle_validation[key]]
            if bad_angles:
                # Find first invalid angle
                first_bad_angle = bad_angles[0]
                # HACK?  Take angle name like "left_neck" and make it words
                # like "left neck"
                first_bad_angle = 'fix ' + first_bad_angle.replace('_', ' ')
                self._play_text(first_bad_angle)
            else:
                # If there's not at least one bad angle, then I think
                # the user never got into a good starting position
                self._play_advice_step(AdviceSteps.FIX_FORM)
        # Was going down and now go up
        elif (prior_feedback == AdviceSteps.DOWN.value.title
              and feedback == AdviceSteps.UP.value.title):
            self._play_advice_step(AdviceSteps.UP)
        # Fixed form
        elif (prior_feedback == AdviceSteps.FIX_FORM.value.title
              and feedback == AdviceSteps.DOWN.value.title):
            self._play_advice_step(AdviceSteps.GOOD)
        elif feedback == 'Good' and prior_feedback != 'Good':
            # This may overlap with previous audio.
            # TODO: Unoverlap this by remembering it for long enough
            self._play_text('Good')
