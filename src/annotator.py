import logging

import numpy as np
from src.annotation_result import AnnotationResult
from src.pose import PoseDetector
from src.pose_landmark import landmarks

logger = logging.getLogger(__name__)


class Annotator:
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
        frame = self.detector.find_pose_and_draw_landmarks(frame, False)
        lm_list = self.detector.find_position(frame, False)
        all_points_in_frame = lm_list and all(
            lm_list[idx].in_frame
            for idx in (landmarks['LEFT_SHOULDER'],
                        landmarks['LEFT_ELBOW'],
                        landmarks['LEFT_WRIST'],
                        landmarks['LEFT_HIP'],
                        landmarks['LEFT_KNEE']))
        # logger.debug(f'in_frame {all_points_in_frame} lm_list {lm_list}')
        logger.debug(f'in_frame {all_points_in_frame}')
        count = 0
        success = False
        angles = {}
        if lm_list:
            for angle in self.movement['angles']:
                # something like "LEFT_SHOULDER,LEFT_ELBOW,LEFT_WRIST"
                recipe_array = angle['recipe'].split(',')

                angles[angle['name']] = self.detector.find_and_draw_angle(
                    frame,
                    landmarks[recipe_array[0]],
                    landmarks[recipe_array[1]],
                    landmarks[recipe_array[2]])

            # Percentage of success of push-up
            self.per = np.interp(angles['elbow'], (90, 160), (0, 100))

            logger.debug(f'elbow {angles["elbow"]} '
                         f'shoulder {angles["shoulder"]} '
                         f'hip {angles["hip"]}')
            # Check to ensure right form before starting the program
            self.right_form = self.right_form or (all_points_in_frame and (
                    angles['elbow'] > 160
                    and angles['shoulder'] > 40
                    and angles['hip'] > 160))

            # Check for full range of motion for the push-up
            if not all_points_in_frame:
                self.feedback = 'Get In Frame'
            elif self.right_form:
                if self.per == 0:
                    if angles['elbow'] <= 90 and angles['hip'] > 160:
                        self.feedback = 'Up'
                        if self.direction == 0:
                            count = 0.5
                            self.direction = 1
                    else:
                        self.feedback = 'Fix Form'
                if self.per == 100:
                    if angles['elbow'] > 160\
                            and angles['shoulder'] > 40\
                            and angles['hip'] > 160:
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
                                self.right_form,
                                success,
                                angles)
