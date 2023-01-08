import logging
import time

from src.advice_steps import AdviceSteps
from src.audio import generate_audio_file, play_audio_file

logger = logging.getLogger(__name__)


class FeedbackGiver:
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
            self, count, rep_completed, target_reps, feedback,
            prior_feedback,
            angle_validation: dict[str, bool]):
        """Give feedback if applicable (i.e. not too often)"""
        logger.debug(f'{count} {target_reps} {feedback} {prior_feedback}')
        seconds_since_audio = time.time() - self._last_audio_time

        # If the count changed, play the new one
        if rep_completed:
            if count == target_reps:
                self._play_advice_step(AdviceSteps.DONE)
            # Give specific count
            elif count > 0:
                self._play_count(count)
            else:
                self._play_advice_step(AdviceSteps.GOOD)
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
