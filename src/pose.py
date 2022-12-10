# This was copied from https://github.com/terminalai/PushUpCounter
import math

import cv2
from src.base import BasePoseDetector


class PoseDetector(BasePoseDetector):
    def find_and_draw_angle(self, img, p1, p2, p3, draw=True):
        assert self.lm_list, 'Call self.find_position first'

        # Get the landmarks
        ll1 = self.lm_list[p1]
        x1, y1 = ll1.x, ll1.y
        ll2 = self.lm_list[p2]
        x2, y2 = ll2.x, ll2.y
        ll3 = self.lm_list[p3]
        x3, y3 = ll3.x, ll3.y

        # Calculate Angle
        angle = math.degrees(math.atan2(y3-y2, x3-x2) -
                             math.atan2(y1-y2, x1-x2))
        if angle < 0:
            angle += 360
            if angle > 180:
                angle = 360 - angle
        elif angle > 180:
            angle = 360 - angle
        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)

            cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)

            cv2.putText(img, str(int(angle)), (x2-50, y2+50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
