import math
import os
import unittest

import cv2
from src.pose import PoseDetector
from src.pose_landmark import (LEFT_ELBOW, LEFT_HIP, LEFT_KNEE, LEFT_SHOULDER,
                               LEFT_WRIST)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestPose(unittest.TestCase):

    def setUp(self):
        pushup_file_name = 'mike_pushup_up_small.jpg'
        # Given a frame of someone starting a push-up
        self.frame = cv2.imread(os.path.join(THIS_DIR, pushup_file_name),
                                cv2.IMREAD_COLOR)

        # When we run the frame through the pose finder
        self.detector = PoseDetector()
        self.frame = self.detector.find_pose_and_draw_landmarks(
            self.frame, False)
        self.detector.find_position(self.frame, False)

    def test_straight_arm_is_near_180_degrees(self):
        # Angle formed from shoulder to elbow to wrist
        angle = self.detector.find_and_draw_angle(
            self.frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST, False)

        # Then we found angle that is within 1 degree of 176
        self.assertTrue(math.isclose(169, angle, abs_tol=1))

    def test_torso_has_acute_angle_with_arm(self):
        # Angle formed from elbow to shoulder to hip
        angle = self.detector.find_and_draw_angle(
            self.frame, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP, False)

        # Then we found angle that is within 1 degree of 66
        self.assertTrue(math.isclose(63, angle, abs_tol=1))

    def test_glutes_inline_with_shoulder_and_knee(self):
        # Angle formed from shoulder to hip to knee
        angle = self.detector.find_and_draw_angle(
            self.frame, LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE, False)

        # Then we found angle that is within 1 degree of 167
        self.assertTrue(math.isclose(179, angle, abs_tol=1))


if __name__ == '__main__':
    unittest.main()
