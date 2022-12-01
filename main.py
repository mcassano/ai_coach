import cv2
import mediapipe as mp
import numpy as np
from threading import Thread
import kritter
import dash_html_components as html
from vizy import Vizy
from annotator import Annotator

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
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            form = 0
            feedback = "Fix Form"
            recordedCount = 0
            annotator = Annotator()
            while self.run_thread:
                frame = self.stream.frame()[0]
                # This was copied from https://github.com/terminalai/PushUpCounter
                success = False
                frame, feedback, count, per, success = annotator.annotateFrameWithDetector(frame)
                if success:
                    self.kapp.push_mods(self.overwrite_text.out_value("%s %s" % (feedback, recordedCount)))

                self.video.push_frame(frame)

if __name__ == "__main__":
    AiCoach()
