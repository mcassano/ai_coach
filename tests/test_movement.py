import os
import unittest

from src.movement import Movement, Requirement, Step

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestMovementExtractor(unittest.TestCase):
    def test_get_list(self):
        self.assertEqual(['Push-up', 'Flapping-Cross'],
                         Movement.get_list_of_movements())

    def test_get_move(self):
        with self.assertRaises(ValueError):
            Movement.get_movement('oops')

        mov = Movement.get_movement('Push-up')
        self.assertEqual('Push-up', mov.name)
        self.assertEqual(10, mov.default_target)


class TestPredicates(unittest.TestCase):
    def test_convert_requirement_to_predicate_true(self):
        req = Requirement({'body': 'elbow', 'test': 'gt', 'angle': 90})
        self.assertTrue(req.test_req('elbow', 100))

    def test_convert_requirement_to_predicate_false(self):
        req = Requirement({'body': 'elbow', 'test': 'gt', 'angle': 90})
        self.assertFalse(req.test_req('elbow', 80))

    def test_convert_requirement_to_predicate_false_equal(self):
        req = Requirement({'body': 'elbow', 'test': 'gt', 'angle': 90})
        self.assertFalse(req.test_req('elbow', 90))

    def test_step_is_validated_all_not_good(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 160},
                        {'body': 'shoulder', 'test': 'gt', 'angle': 40},
                        {'body': 'hip', 'test': 'gt', 'angle': 160}
                        ]
        angles = {'elbow': 80,
                  'shoulder': 90,
                  'hip': 100
                  }
        step = Step({'name': 'step1', 'requirement': requirements})
        self.assertFalse(step.is_validated(angles))

    def test_step_is_validated_one_not_good(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 160},
                        {'body': 'shoulder', 'test': 'gt', 'angle': 40},
                        {'body': 'hip', 'test': 'gt', 'angle': 160}
                        ]
        angles = {'elbow': 170,
                  'shoulder': 50,
                  'hip': 100
                  }
        step = Step({'name': 'step1', 'requirement': requirements})
        self.assertFalse(step.is_validated(angles))

    def test_step_is_validated_all_good(self):
        requirements = [{'body': 'elbow', 'test': 'gt', 'angle': 160},
                        {'body': 'shoulder', 'test': 'gt', 'angle': 40},
                        {'body': 'hip', 'test': 'gt', 'angle': 160}
                        ]
        angles = {'elbow': 170,
                  'shoulder': 45,
                  'hip': 190
                  }
        step = Step({'name': 'step1', 'requirement': requirements})
        self.assertTrue(step.is_validated(angles))
