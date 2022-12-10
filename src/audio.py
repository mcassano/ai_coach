import logging
import os.path
import time

from gtts import gTTS
from playsound import playsound
from src.advice_steps import AdviceSteps

logger = logging.getLogger(__name__)


class Audio:
    def __init__(self):
        self._last_audio_time = time.time()

    def _play_audio_file(self, path: str):
        playsound(path, block=False)
        self._last_audio_time = time.time()

    def _play_advice_step(self, step: AdviceSteps):
        self._play_audio_file(step.value.audio_path)

    def _play_count(self, count):
        path = f'./audio/count/{count}.mp3'
        if not os.path.exists(path):
            # generate count audio
            tts = gTTS(str(count), lang='en', slow=False)
            tts.save(path)
        self._play_audio_file(path)

    def play_sound_if_applicable(self, count, target, feedback,
                                 prior_feedback):
        logger.debug(f'{count} {target} {feedback} {prior_feedback}')
        seconds_since_audio = time.time() - self._last_audio_time

        # Get in Frame but only after some seconds
        if (feedback == AdviceSteps.GET_IN_FRAME.value.title
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
        # Was coming up and completed a rep
        elif (prior_feedback == AdviceSteps.UP.value.title
              and feedback == AdviceSteps.DOWN.value.title):
            if count == target:
                self._play_advice_step(AdviceSteps.DONE)
            # Give specific count
            elif count > 0:
                self._play_count(count)
            else:
                self._play_advice_step(AdviceSteps.GOOD)
        # Fixed form
        elif (prior_feedback == AdviceSteps.FIX_FORM.value.title
              and feedback == AdviceSteps.DOWN.value.title):
            self._play_advice_step(AdviceSteps.GOOD)
