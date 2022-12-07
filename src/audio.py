import logging
import os.path
import time

from gtts import gTTS
from playsound import playsound
from src.advice_steps import AdviceSteps

logger = logging.getLogger(__name__)


def play_audio_file_unblocking(path):
    playsound(path, block=False)


class Audio:
    def __init__(self):
        self.time_since_last_audio = time.time()

    def play_sound_if_applicable(self, count, target, feedback,
                                 prior_feedback):
        logger.debug(f'{count} {target} {feedback} {prior_feedback}')
        # Get in Frame but only after some seconds
        if (feedback == AdviceSteps.GET_IN_FRAME.value.title
                and time.time() - self.time_since_last_audio > 2):
            play_audio_file_unblocking(
                AdviceSteps.GET_IN_FRAME.value.audio_path)
            self.time_since_last_audio = time.time()
        # Fix form but only after some seconds
        elif (feedback == AdviceSteps.FIX_FORM.value.title
              and time.time() - self.time_since_last_audio > 2):
            play_audio_file_unblocking(AdviceSteps.FIX_FORM.value.audio_path)
            self.time_since_last_audio = time.time()
        # Was going down and now go up
        elif (prior_feedback == AdviceSteps.DOWN.value.title
              and feedback == AdviceSteps.UP.value.title):
            play_audio_file_unblocking(AdviceSteps.UP.value.audio_path)
            self.time_since_last_audio = time.time()
        # Was coming up and completed a rep
        elif (prior_feedback == AdviceSteps.UP.value.title
              and feedback == AdviceSteps.DOWN.value.title):
            if count == target:
                play_audio_file_unblocking(AdviceSteps.DONE.value.audio_path)
            # Give specific count every quarter of target
            elif count % (target / 4) == 0:
                path = './audio/count/%d.mp3' % count
                if not os.path.exists(path):
                    tts = gTTS(text='%d' % count, lang='en', slow=False)
                    tts.save(path)
                play_audio_file_unblocking(path)
            else:
                play_audio_file_unblocking(AdviceSteps.GOOD.value.audio_path)
            self.time_since_last_audio = time.time()
        # Fixed form
        elif (prior_feedback == AdviceSteps.FIX_FORM.value.title
              and feedback == AdviceSteps.DOWN.value.title):
            play_audio_file_unblocking(AdviceSteps.GOOD.value.audio_path)
            self.time_since_last_audio = time.time()
