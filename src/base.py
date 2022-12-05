# This was copied from https://github.com/terminalai/PushUpCounter
from dataclasses import dataclass

import cv2
import mediapipe as mp


@dataclass
class LandmarkLabel:
    landmark_id: int
    x: int
    y: int
    in_frame: bool


class BasePoseDetector:
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                 enable_segmentation=False, smooth_segmentation=True,
                 detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detection_con = detection_con
        self.track_con = track_con

        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            self.mode, self.complexity, self.smooth_landmarks,
            self.enable_segmentation, self.smooth_segmentation,
            self.detection_con, self.track_con)
        self.results = None
        self.lm_list = []

    def find_pose_and_draw_landmarks(self, img, draw=True):
        """Return img with landmarks drawn (if draw=True).

        :param img  cv2 image (i.e. BGR)
        :param draw  If true, draw landmarks on img before returning it

        Also store pose landmarks in self.results."""
        # pose.process takes RGB
        img_rgb = img[:, :, ::-1]
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks and draw:
            self.mp_draw.draw_landmarks(img, self.results.pose_landmarks,
                                        self.mp_pose.POSE_CONNECTIONS)

        return img

    def find_position(self, img, draw=True):
        self.lm_list = []
        if self.results.pose_landmarks:
            for the_id, lm in enumerate(self.results.pose_landmarks.landmark):
                # finding height, width of the image printed
                h, w, _c = img.shape
                # Determining the pixels of the landmarks
                cx, cy = int(lm.x * w), int(lm.y * h)
                in_frame = 0 <= lm.x <= 1 and 0 <= lm.y <= 1
                self.lm_list.append(LandmarkLabel(the_id, cx, cy, in_frame))
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lm_list


def main():
    detector = BasePoseDetector()
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        # ret is just the return variable, not much in there that we will use.
        if ret:
            img = detector.find_pose_and_draw_landmarks(img)
            cv2.imshow('Pose Detection', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
