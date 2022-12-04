from enum import Enum

from advice import Advice


class AdviceSteps(Enum):
    GET_IN_FRAME = Advice('Get In Frame', './audio/get_in_frame.mp3')
    FIX_FORM = Advice('Fix Form', './audio/fix_form.mp3')
    GOOD = Advice('Good', './audio/good.mp3')
    UP = Advice('Up', './audio/up.mp3')
    DOWN = Advice('Down', './audio/down.mp3')
    DONE = Advice('Done', './audio/done.mp3')
