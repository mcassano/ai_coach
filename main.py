import cv2
import mediapipe as mp
from threading import Thread
import kritter
import dash_html_components as html
from vizy import Vizy

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

CAMERA_MODE = "1280x720x10bpp"
CAMERA_WIDTH = 1280
STREAM_WIDTH = 1280

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

        self.kapp.layout = html.Div([html.Div([self.video])], style={"padding": "15px"})

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
            while self.run_thread:
                frame = self.stream.frame()[0]
                
                results = pose.process(frame)
                
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                self.video.push_frame(frame)

if __name__ == "__main__":
    AiCoach()
