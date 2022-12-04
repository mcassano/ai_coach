#!/usr/bin/env python

# Us
import argparse

# Them
import cv2

from annotator import Annotator
from audio import Audio
from display import Display
from movement_extractor import MovementExtractor
from pose import PoseDetector
from util import logging_basic_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log-level', '-l', help='log level',
        choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument(
        '--movement', '-m', help='Movement name', default='Push-up',
        choices=['Push-up'])
    parser.add_argument(
        '--video-file', help='File with video of exercise (example: file.mp4)')
    args = parser.parse_args()

    logging_basic_config(args.log_level)

    annotator = Annotator()
    audio = Audio()
    movement = MovementExtractor.get_movement(args.movement)
    display = Display('AI Coach')
    detector = PoseDetector()

    print("Using '%s' movement" % movement['name'])

    capture_input = args.video_file
    if not capture_input:
        # live capture from camera 0
        capture_input = 0
    cap = cv2.VideoCapture(capture_input)
    feedback = 'Fix Form'
    target = movement['end_at']
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            prior_feedback = feedback
            result = annotator.annotate_frame_with_detector(frame, detector)
            feedback = result.feedback

            display.display_result(result)

            audio.play_sound_if_applicable(
                result.count, target, result.feedback, prior_feedback)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    display.close()


if __name__ == '__main__':
    main()
