import unittest

from src.feedback_giver import FeedbackGiver


class TestAudio(unittest.TestCase):
    # pylint: disable-next=no-self-use
    def test_play_count(self):
        audio = FeedbackGiver()
        # pylint: disable-next=protected-access
        audio._play_count(3)
