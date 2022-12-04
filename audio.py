import os.path
import time

from gtts import gTTS
from playsound import playsound


class Audio:
    def __init__(self):
        self.time_since_last_audio = time.time()

    def play_sound_if_applicable(self, count, target, feedback,
                                 prior_feedback):
        # Fix form but only after some seconds so that you don't get
        # hammered over and over
        if (feedback == 'Fix Form'
                and time.time() - self.time_since_last_audio > 2):
            playsound('./audio/fix_form.mp3')
            self.time_since_last_audio = time.time()
        # Was going down and now go up
        elif prior_feedback == 'Down' and feedback == 'Up':
            playsound('./audio/up.mp3')
            self.time_since_last_audio = time.time()
        # Was coming up and completed a rep
        elif prior_feedback == 'Up' and feedback == 'Down':
            if count == target:
                playsound('./audio/done.mp3')
            # Give specific count every quarter of target
            elif count % (target / 4) == 0:
                path = './audio/count/%d.mp3' % (count)
                if not os.path.exists(path):
                    tts = gTTS(text='%d' % (count), lang='en', slow=False)
                    tts.save(path)
                playsound(path)
            else:
                playsound('./audio/good.mp3')
            self.time_since_last_audio = time.time()
        # Fixed form
        elif prior_feedback == 'Fix Form' and feedback == 'Down':
            playsound('./audio/good.mp3')
            self.time_since_last_audio = time.time()
