from enum import Enum

from src.advice import Advice


class AdviceSteps(Enum):
    GET_IN_FRAME = Advice('Get In Frame', 'get_in_frame.mp3')
    FIX_FORM = Advice('Fix Form', 'fix_form.mp3')
    GOOD = Advice('Good', 'good.mp3')
    UP = Advice('Up', 'up.mp3')
    DOWN = Advice('Down', 'down.mp3')
    DONE = Advice('Done', 'done.mp3')
