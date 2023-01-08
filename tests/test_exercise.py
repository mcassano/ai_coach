import os
from unittest import TestCase

from src.exercise import Angle, Exercise, Pose, Requirement, Step

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestExerciseExtractor(TestCase):
    def test_get_list(self):
        self.assertEqual(['Push-up', 'Flapping-Cross', 'Plank'],
                         Exercise.exercise_names())

    def test_get_move(self):
        with self.assertRaises(KeyError):
            Exercise.exercise('oops')

        mov = Exercise.exercise('Push-up')
        self.assertEqual('Push-up', mov.name)
        self.assertEqual(10, mov.default_target_reps)

    def test_plank(self):
        exer = Exercise.exercise('Plank')
        self.assertEqual('Plank', exer.name)
        self.assertEqual(1, len(exer.steps))
        self.assertEqual(30, exer.steps[0].default_target_seconds)


class TestAngle(TestCase):
    def test_angle(self):
        angle = Angle('left_elbow', 'LEFT_SHOULDER,LEFT_ELBOW,LEFT_WRIST')
        self.assertEqual('left_elbow', angle.name)
        self.assertEqual([11, 13, 15], angle.landmark_indexes)


class TestPredicates(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.all_angles = {
            'left_elbow': Angle(
                'left_elbow', 'LEFT_SHOULDER,LEFT_ELBOW,LEFT_WRIST'),
            'left_shoulder': Angle(
                'left_shoulder', 'LEFT_ELBOW,LEFT_SHOULDER,LEFT_HIP'),
            'left_hip': Angle('left_hip', 'LEFT_SHOULDER,LEFT_HIP,LEFT_KNEE'),
            }
        self.all_poses = {
            'pushup up': Pose(
                'pushup up',
                [
                    {
                        'body_angle': 'left_elbow',
                        'test': 'gt',
                        'angle': 160
                    },
                    {
                        'body_angle': 'left_shoulder',
                        'test': 'gt',
                        'angle': 40
                    },
                    {
                        'body_angle': 'left_hip',
                        'test': 'gt',
                        'angle': 160
                    }
                ],
                self.all_angles
            ),
            'plank on elbows': Pose(
                'plank on elbows',
                [
                    {
                        'body_angle': 'left_elbow',
                        'test': 'near',
                        'angle': 90,
                        'near_degrees': 5
                    },
                    {
                        'body_angle': 'left_shoulder',
                        'test': 'near',
                        'angle': 90,
                        'near_degrees': 5
                    },
                    {
                        'body_angle': 'left_hip',
                        'test': 'near',
                        'angle': 180,
                        'near_degrees': 5
                    },
                ],
                self.all_angles),
        }

    def test_convert_requirement_to_predicate_true(self):
        req = Requirement(
            {'body_angle': 'left_elbow', 'test': 'gt', 'angle': 90},
            all_angles=self.all_angles)
        self.assertTrue(req.test_req('left_elbow', 100))

    def test_near_true(self):
        req = Requirement(
            {'body_angle': 'left_elbow', 'test': 'near',
             'angle': 90, 'near_degrees': 5},
            all_angles=self.all_angles)
        self.assertTrue(req.test_req('left_elbow', 92))

        req = Requirement(
            {'body_angle': 'left_elbow', 'test': 'near',
             'angle': 90, 'near_degrees': 10},
            all_angles=self.all_angles)
        self.assertTrue(req.test_req('left_elbow', 98))

    def test_convert_requirement_to_predicate_false(self):
        req = Requirement(
            {'body_angle': 'left_elbow', 'test': 'gt', 'angle': 90},
            all_angles=self.all_angles)
        self.assertFalse(req.test_req('left_elbow', 80))

    def test_near_false(self):
        req = Requirement(
            {'body_angle': 'left_elbow', 'test':
                'near', 'angle': 90, 'near_degrees': 5},
            all_angles=self.all_angles)
        self.assertFalse(req.test_req('left_elbow', 98))

    def test_convert_requirement_to_predicate_false_equal(self):
        req = Requirement(
            {'body_angle': 'left_elbow', 'test': 'gt', 'angle': 90},
            all_angles=self.all_angles)
        self.assertFalse(req.test_req('left_elbow', 90))

    def test_step_is_validated_all_not_good(self):
        angles = {'left_elbow': 80,
                  'left_shoulder': 39,
                  'left_hip': 100
                  }
        step = Step({'name': 'step1', 'pose': 'pushup up'},
                    all_poses=self.all_poses)
        self.assertFalse(step.pose.is_validated(angles))
        self.assertEqual(
            {'left_elbow': False, 'left_hip': False, 'left_shoulder': False},
            step.pose.validation_result(angles))

    def test_step_is_validated_one_not_good(self):
        angles = {'left_elbow': 170,
                  'left_shoulder': 50,
                  'left_hip': 100
                  }
        step = Step({'name': 'step1', 'pose': 'pushup up'},
                    all_poses=self.all_poses)
        self.assertFalse(step.pose.is_validated(angles))
        self.assertEqual(
            {'left_elbow': True, 'left_hip': False, 'left_shoulder': True},
            step.pose.validation_result(angles))

    def test_step_is_validated_all_good(self):
        angles = {'left_elbow': 170,
                  'left_shoulder': 45,
                  'left_hip': 190
                  }
        step = Step({'name': 'step1', 'pose': 'pushup up'},
                    all_poses=self.all_poses)
        self.assertTrue(step.pose.is_validated(angles))
        self.assertEqual(
            {'left_elbow': True, 'left_hip': True, 'left_shoulder': True},
            step.pose.validation_result(angles))

    def test_plank_is_validated_all_good(self):
        angles = {'left_elbow': 92,
                  'left_shoulder': 92,
                  'left_hip': 182
                  }
        step = Step({'name': 'step1', 'pose': 'plank on elbows'},
                    all_poses=self.all_poses)
        self.assertTrue(step.pose.is_validated(angles))
