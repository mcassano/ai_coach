import os
import unittest

import cv2
from src.annotator import Annotator
from src.pose import PoseDetector

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_frame(path):
    return cv2.imread(os.path.join(THIS_DIR, path),
                      cv2.IMREAD_COLOR)


class TestAnnotator(unittest.TestCase):

    def setUp(self):
        self.pushup_up_file_name = 'mike_pushup_up_small.jpg'
        self.pushup_down_file_name = 'mike_pushup_down_small.jpg'

        # When we run the frame through the pose finder
        self.detector = PoseDetector()

    def test_up_down_up_down_good_results(self):
        annotator = Annotator([])

        # Go up-down ten times and check that the results are correct
        for idx in range(0, 5):
            for _ in range(0, 5):
                annotator.annotate_frame(
                    load_frame(self.pushup_up_file_name))
            result = annotator.annotate_frame(
                load_frame(self.pushup_up_file_name))
            self.check_results([idx, 'Down', True, 100.0, True], result)

            for _ in range(0, 5):
                annotator.annotate_frame(
                    load_frame(self.pushup_down_file_name))
            result = annotator.annotate_frame(
                load_frame(self.pushup_down_file_name))
            self.check_results([idx + 0.5, 'Up', True, 0.0, True], result)

    def check_results(self, expected, actual):
        self.assertEqual(expected[0], actual.count)
        self.assertEqual(expected[1], actual.feedback)
        self.assertEqual(expected[2], actual.form)
        self.assertEqual(expected[3], actual.per)
        self.assertEqual(expected[4], actual.success)


if __name__ == '__main__':
    unittest.main()
