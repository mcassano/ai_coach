from threading import Thread

import dash_html_components as html
import kritter
from vizy import Vizy

from annotator import Annotator
from pose import PoseDetector

CAMERA_MODE = '1280x720x10bpp'
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
        self.overwrite_text = kritter.Ktext(
            value='Loading...', style={'control_width': 12})
        self.kapp.layout = html.Div(
            [html.Div([self.video, self.overwrite_text])], style={
                'padding': '15px', 'font-size': '6em'})

        # Run camera grab thread.
        self.run_thread = True
        self._grab_thread = Thread(target=self.add_pose)
        self._grab_thread.start()

        # Run Kritter server, which blocks.
        self.kapp.run()
        self.run_thread = False
        self._grab_thread.join()

    def add_pose(self):
        # form = 0
        feedback = 'Fix Form'
        recorded_count = 0.0
        # direction = 0
        annotator = Annotator()
        detector = PoseDetector()
        self.kapp.push_mods(self.overwrite_text.out_value(
            '%s %s' % (feedback, recorded_count)))
        while self.run_thread:
            frame = self.stream.frame()[0]
            # This was copied from https://github.com/terminalai/PushUpCounter
            (annotated_frame, new_feedback, new_count, _per, _direction, _bar,
             success) = annotator.annotateFrameWithDetector(frame, detector)
            if success:
                frame = annotated_frame
                if new_count != recorded_count or (
                        new_feedback != '' and new_feedback != feedback):
                    recorded_count = new_count
                    feedback = new_feedback
                    self.kapp.push_mods(self.overwrite_text.out_value(
                        '%s %s' % (feedback, recorded_count)))

            self.video.push_frame(frame)


if __name__ == '__main__':
    AiCoach()
