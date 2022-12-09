import os
import unittest

from src.movement_extractor import MovementExtractor

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestMovementExtractor(unittest.TestCase):
    def test_get_list(self):
        self.assertEqual(['Push-up', 'Flapping-Cross'],
                         MovementExtractor.get_list_of_movements())

    def test_get_move(self):
        with self.assertRaises(ValueError):
            MovementExtractor.get_movement('oops')

        mov = MovementExtractor.get_movement('Push-up')
        self.assertEqual('Push-up', mov['name'])
