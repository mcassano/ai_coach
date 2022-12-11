import unittest

from src.audio import Audio


class TestAudio(unittest.TestCase):
    # pylint: disable-next=no-self-use
    def test_play_count(self):
        audio = Audio()
        # pylint: disable-next=protected-access
        audio._play_count(3)
