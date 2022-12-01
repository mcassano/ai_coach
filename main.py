import cv2
import mediapipe as mp
import numpy as np
from threading import Thread
import kritter
import dash_html_components as html
from vizy import Vizy
from pose import PoseDetector

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

CAMERA_MODE = "1280x720x10bpp"
CAMERA_WIDTH = 1280
STREAM_WIDTH = 800

class AiCoach:
    def __init__(self):
        self.kapp = Vizy()

        # Create and start camera.
        self.camera = kritter.Camera(hflip=True, vflip=True, mem_reserve=50)
        self.stream = self.camera.stream()
        self.camera.mode = CAMERA_MODE
        self.camera.brightness = 50
        self.camera.framerate = 30  
        self.camera.autoshutter = True
        self.camera.awb = True

        self.video = kritter.Kvideo(width=STREAM_WIDTH, overlay=True)
        self.overwrite_text = kritter.Ktext(value="Mike", style={"control_width": 12})
        self.kapp.layout = html.Div([html.Div([self.video, self.overwrite_text])], style={"padding": "15px", "font-size": "6em"})

        # Run camera grab thread.
        self.run_thread = True
        self._grab_thread = Thread(target=self.add_pose)
        self._grab_thread.start()

        # Run Kritter server, which blocks.
        self.kapp.run()
        self.run_thread = False
        self._grab_thread.join()

    def add_pose(self):
        detector = PoseDetector()
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            count = 0
            direction = 0
            form = 0
            feedback = "Fix Form"
            recordedCount = 0
            while self.run_thread:
                frame = self.stream.frame()[0]
                # This was copied from https://github.com/terminalai/PushUpCounter
                frame = detector.findPose(frame, False)
                lmList = detector.findPosition(frame, False)
                if len(lmList) != 0:
                    elbow = detector.findAngle(frame, 11, 13, 15)
                    shoulder = detector.findAngle(frame, 13, 11, 23)
                    hip = detector.findAngle(frame, 11, 23,25)

                    #Percentage of success of pushup
                    per = np.interp(elbow, (90, 160), (0, 100))

                    #Bar to show Pushup progress
                    bar = np.interp(elbow, (90, 160), (380, 50))

                    #Check to ensure right form before starting the program
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        form = 1

                    #Check for full range of motion for the pushup
                    if form == 1:
                        if per == 0:
                            if elbow <= 90 and hip > 160:
                                feedback = "Up"
                                if direction == 0:
                                    count += 0.5
                                    direction = 1
                            else:
                                feedback = "Fix Form"
                        if per == 100:
                            if elbow > 160 and shoulder > 40 and hip > 160:
                                feedback = "Down"
                                if direction == 1:
                                    count += 0.5
                                    direction = 0
                            else:
                                feedback = "Fix Form"

                    if count != recordedCount:
                        print(count)

                    recordedCount = count
                self.kapp.push_mods(self.overwrite_text.out_value("%s %s" % (feedback, recordedCount)))

                self.video.push_frame(frame)

if __name__ == "__main__":
    AiCoach()
