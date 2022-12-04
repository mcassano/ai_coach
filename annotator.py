import logging

import numpy as np

from annotation_result import AnnotationResult
from pose_landmark import (LEFT_ELBOW, LEFT_HIP, LEFT_KNEE, LEFT_SHOULDER,
                           LEFT_WRIST)

logger = logging.getLogger(__name__)


class Annotator():
    def __init__(self):
        self.recorded_count = 0
        self.direction = 0
        self.feedback = ''
        self.form = 0
        self.per = 0

    def annotate_frame_with_detector(self, frame, detector):
        # This was copied from https://github.com/terminalai/PushUpCounter
        frame = detector.find_pose(frame, False)
        lm_list = detector.find_position(frame, False)
        logger.debug(f'lm_list {lm_list}')
        count = 0
        bar = 0
        success = False
        if len(lm_list) != 0:
            elbow = detector.find_angle(
                frame, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
            shoulder = detector.find_angle(
                frame, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
            hip = detector.find_angle(
                frame, LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE)

            # Percentage of success of pushup
            self.per = np.interp(elbow, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            logger.debug(f'elbow {elbow} shoulder {shoulder} hip {hip}')
            # Check to ensure right form before starting the program
            if elbow > 160 and shoulder > 40 and hip > 160:
                self.form = 1

            # Check for full range of motion for the pushup
            if self.form == 1:
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

        return AnnotationResult(frame,
                                self.feedback,
                                self.recorded_count,
                                self.per,
                                self.direction,
                                bar,
                                self.form,
                                success)
