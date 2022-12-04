import logging

import numpy as np

from annotation_result import AnnotationResult
from pose import PoseDetector
from pose_landmark import (LEFT_ELBOW, LEFT_HIP, LEFT_KNEE, LEFT_SHOULDER,
                           LEFT_WRIST)

logger = logging.getLogger(__name__)


class Annotator():
    def __init__(self, movement):
        self.recorded_count = 0
        self.direction = 0
        self.feedback = ''
        self.per = 0
        self.detector = PoseDetector()
        self.movement = movement
        self.right_form = False

    def annotate_frame(self, frame):
        # This was inspired from https://github.com/terminalai/PushUpCounter
        frame = self.detector.find_pose(frame, False)
        lm_list = self.detector.find_position(frame, False)
        all_points_in_frame = lm_list and all(
            lm_list[idx].in_frame
            for idx in (LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST,
                        LEFT_HIP, LEFT_KNEE))
        # logger.debug(f'in_frame {all_points_in_frame} lm_list {lm_list}')
        logger.debug(f'in_frame {all_points_in_frame}')
        count = 0
        bar = 0
        success = False
        if lm_list:
            elbow = self.detector.find_and_draw_angle(
                frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
            shoulder = self.detector.find_and_draw_angle(
                frame, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
            hip = self.detector.find_and_draw_angle(
                frame, LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE)

            # Percentage of success of push-up
            self.per = np.interp(elbow, (90, 160), (0, 100))

            # Bar to show Push-up progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            logger.debug(f'elbow {elbow} shoulder {shoulder} hip {hip}')
            # Check to ensure right form before starting the program
            self.right_form = self.right_form or (all_points_in_frame and (
                    elbow > 160 and shoulder > 40 and hip > 160))

            # Check for full range of motion for the push-up
            if not all_points_in_frame:
                self.feedback = 'Get In Frame'
            elif self.right_form:
                if self.per == 0:
                    if elbow <= 90 and hip > 160:
                        self.feedback = 'Up'
                        if self.direction == 0:
                            count = 0.5
                            self.direction = 1
                    else:
                        self.feedback = 'Fix Form'
                if self.per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        self.feedback = 'Down'
                        if self.direction == 1:
                            count = 0.5
                            self.direction = 0
                    else:
                        self.feedback = 'Fix Form'
            else:
                self.feedback = 'Fix Form'

            self.recorded_count = self.recorded_count + count
            success = True
        else:
            logger.debug('annotate frame found no pose ..')

        logger.debug(f'\'{self.feedback}\' \'{self.recorded_count}\'')
        return AnnotationResult(frame,
                                self.feedback,
                                self.recorded_count,
                                self.per,
                                self.direction,
                                bar,
                                self.right_form,
                                success)
