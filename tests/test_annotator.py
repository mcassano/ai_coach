import collections
import os
import unittest

import cv2
from src.annotator import Annotator
from src.movement_extractor import MovementExtractor
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
        annotator = Annotator(MovementExtractor.get_movement('Push-up'))

        # Go up-down several times and check that the results are correct
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

    def test_parts_from_all_recipes(self):
        angles = [{'recipe': 'A,B,C,D'}, {'recipe': 'A,C'}, {'recipe': 'D'}]
        result = Annotator.parts_from_all_recipes(angles)
        self.assertTrue(
            collections.Counter(['A', 'B', 'C', 'D'])
            == collections.Counter(result))

    def test_landmark_indices_from_parts(self):
        parts = ['NOSE', 'MOUTH_RIGHT', 'LEFT_PINKY']
        result = Annotator.landmark_indices_from_parts(parts)
        self.assertTrue(
            collections.Counter([0, 17, 10])
            == collections.Counter(result))

    def test_convert_requirement_to_predicate_true(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 90}]
        result = Annotator.covert_requirement_to_predicate(requirements,
                                                           'elbow',
                                                           100)
        self.assertTrue(result)

    def test_convert_requirement_to_predicate_false(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 90}]
        result = Annotator.covert_requirement_to_predicate(requirements,
                                                           'elbow',
                                                           80)
        self.assertFalse(result)

    def test_convert_requirement_to_predicate_false_equal(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 90}]
        result = Annotator.covert_requirement_to_predicate(requirements,
                                                           'elbow',
                                                           90)
        self.assertFalse(result)

    def test_step_is_validated_all_not_good(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 160},
                        {'body': 'shoulder', 'test': 'gt', 'angle': 40},
                        {'body': 'hip', 'test': 'gt', 'angle': 160}
                        ]
        angles = {'elbow': 80,
                  'shoulder': 90,
                  'hip': 100
                  }
        result = Annotator.step_is_validated(requirements, angles)
        self.assertFalse(result)

    def test_step_is_validated_one_not_good(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 160},
                        {'body': 'shoulder', 'test': 'gt', 'angle': 40},
                        {'body': 'hip', 'test': 'gt', 'angle': 160}
                        ]
        angles = {'elbow': 170,
                  'shoulder': 50,
                  'hip': 100
                  }
        result = Annotator.step_is_validated(requirements, angles)
        self.assertFalse(result)

    def test_step_is_validated_all_good(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 160},
                        {'body': 'shoulder', 'test': 'gt', 'angle': 40},
                        {'body': 'hip', 'test': 'gt', 'angle': 160}
                        ]
        angles = {'elbow': 170,
                  'shoulder': 45,
                  'hip': 190
                  }
        result = Annotator.step_is_validated(requirements, angles)
        self.assertTrue(result)

    def check_results(self, expected, actual):
        self.assertEqual(expected[0], actual.count)
        self.assertEqual(expected[1], actual.feedback)
        self.assertEqual(expected[2], actual.form)
        self.assertEqual(expected[3], actual.per)
        self.assertEqual(expected[4], actual.success)


if __name__ == '__main__':
    unittest.main()
