#!/usr/bin/env python

import argparse
import time
from collections import deque

import cv2
from src.annotator import Annotator
from src.audio import play_text
from src.display import Display
from src.exercise import Exercise
from src.feedback_giver import FeedbackGiver
from src.util import logging_basic_config


class FramesPerSecond:
    """Track frames per second"""
    def __init__(self):
        # last 5 times
        self.times = deque(maxlen=5)

    def take_sample(self):
        self.times.appendleft(time.time())

    def most_recent_time(self):
        return self.times[0]

    def frames_per_second(self):
        """Return frames per second if there are enough samples."""
        # TODO: check that this is correct
        num_times = len(self.times)
        fps = None
        if num_times >= 5:
            prev_time = self.times.pop()
            the_time = self.times[0]
            fps = (num_times - 1) / (
                    the_time - prev_time)
        return fps


def main():
    args = run_argument_parser()

    logging_basic_config(args.log_level)

    exercise = Exercise.exercise(args.exercise)
    target_reps = (args.target_reps
                   if args.target_reps is not None
                   else exercise.default_target_reps)
    target_seconds = (args.target_seconds
                      if args.target_seconds is not None
                      else exercise.default_target_seconds)

    annotator = Annotator(exercise, target_seconds)
    feedback_giver = FeedbackGiver()
    display = Display('AI Coach')

    play_text(args.exercise, block=True)

    capture_input = args.video_file
    if not capture_input:
        # live capture from camera 0
        capture_input = 0
    cap = cv2.VideoCapture(capture_input)
    print(f'Using {exercise.name} exercise, target_reps: {target_reps}')
    fps = FramesPerSecond()
    last_fps_print = 0
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            result = annotator.annotate_frame(frame)
            display.display_result(result)

            feedback_giver.give_feedback(
                result.exercise_num_steps,
                result.rep_count,
                result.rep_completed,
                target_reps,
                result.right_form_seconds,
                result.feedback,
                result.angle_validation)

            # Frames per second
            if args.show_frames_per_second:
                fps.take_sample()
                the_fps = fps.frames_per_second()
                if the_fps and (fps.most_recent_time() - last_fps_print) > 1:
                    print(f'{the_fps:.2f} frames per second')
                    last_fps_print = fps.most_recent_time()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    display.close()


def run_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log-level', '-l', help='log level',
        choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument(
        '--exercise', '-e', help='Exercise name', required=True,
        choices=Exercise.exercise_names())
    parser.add_argument(
        '--video-file', help='File with video of exercise (example: file.mp4)')
    parser.add_argument(
        '--target-reps', type=int,
        help='The number of reps you would like to complete (example: 20)')
    parser.add_argument(
        '--target-seconds', type=int,
        help='The number of seconds you would like to hold (example: 20)')
    parser.add_argument(
        '--show-frames-per-second', '--fps',
        action='store_true',
        help='Show frames per second')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
