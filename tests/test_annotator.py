import os
import time
import unittest

import cv2
from src.annotator import Annotator
from src.exercise import Exercise
from src.pose import PoseDetector

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def load_frame(path):
    return cv2.imread(os.path.join(THIS_DIR, path),
                      cv2.IMREAD_COLOR)


class TestAnnotator(unittest.TestCase):

    def setUp(self):
        self.pushup_up_file_name = 'mike_pushup_up_small.jpg'
        self.pushup_down_file_name = 'mike_pushup_down_small.jpg'
        self.plank_file_name = 'dan_plank.jpg'

        # When we run the frame through the pose finder
        self.detector = PoseDetector()

    def test_up_down_up_down_good_results(self):
        annotator = Annotator(Exercise.exercise('Push-up'),
                              static_image_mode=True)

        # Go up-down several times and check that the results are correct
        for idx in range(0, 5):
            result = annotator.annotate_frame(
                load_frame(self.pushup_up_file_name))
            self.check_results([idx, 'Down', True, 100.0, True], result)

            result = annotator.annotate_frame(
                load_frame(self.pushup_down_file_name))
            self.check_results([idx + 0.5, 'Up', True, 0.0, True], result)

    def test_plank_good_results(self):
        exer = Exercise.exercise('Plank')
        # only hold plank for one second for testing
        exer.steps[0].target_seconds = 1
        annotator = Annotator(exer, static_image_mode=True)

        # First time plank is seen, form is good but not long enough
        result = annotator.annotate_frame(load_frame(self.plank_file_name))
        self.assertEqual(0, result.rep_count)
        self.assertEqual('Hold', result.feedback)
        self.assertTrue(result.right_form)
        self.assertFalse(result.rep_completed)
        self.assertEqual(0, result.right_form_seconds)

        # After waiting a second, rep is completed
        time.sleep(1)
        result = annotator.annotate_frame(load_frame(self.plank_file_name))
        self.assertEqual(1, result.rep_count)
        self.assertEqual('Done', result.feedback)
        self.assertTrue(result.right_form)
        self.assertTrue(result.rep_completed)
        self.assertEqual(1, result.right_form_seconds)

    def check_results(self, expected, actual):
        self.assertEqual(expected[0], actual.rep_count)
        self.assertEqual(expected[1], actual.feedback)
        self.assertEqual(expected[2], actual.right_form)
        self.assertEqual(expected[3], actual.per)
        self.assertEqual(expected[4], actual.success)


if __name__ == '__main__':
    unittest.main()
