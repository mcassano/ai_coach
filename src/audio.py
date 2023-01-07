import logging
import os.path
import time

from gtts import gTTS
from playsound import playsound
from src.advice_steps import AdviceSteps

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)


class Audio:
    def __init__(self):
        self._last_audio_time = 0

    @staticmethod
    def _audio_full_path(path):
        return os.path.join(THIS_DIR, '../audio', path)

    def _play_audio_file(self, path: str):
        playsound(self._audio_full_path(path), block=False)
        logger.debug(f'Play audio {path}')
        self._last_audio_time = time.time()

    def _play_advice_step(self, step: AdviceSteps):
        self._play_audio_file(step.value.audio_path)

    def _play_count(self, count):
        # make sure count isn't a decimal: 1.0 --> 1
        count = int(count)
        path = f'count/{count}.mp3'
        fullpath = self._audio_full_path(path)
        if not os.path.exists(fullpath):
            # generate count audio
            tts = gTTS(str(count), lang='en', slow=False)
            tts.save(fullpath)

        self._play_audio_file(path)

    def play_sound_if_applicable(
            self, count, rep_completed, target_reps, feedback,
            prior_feedback):
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
            self._play_advice_step(AdviceSteps.FIX_FORM)
        # Was going down and now go up
        elif (prior_feedback == AdviceSteps.DOWN.value.title
              and feedback == AdviceSteps.UP.value.title):
            self._play_advice_step(AdviceSteps.UP)
        # Fixed form
        elif (prior_feedback == AdviceSteps.FIX_FORM.value.title
              and feedback == AdviceSteps.DOWN.value.title):
            self._play_advice_step(AdviceSteps.GOOD)
