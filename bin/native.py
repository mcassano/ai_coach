#!/usr/bin/env python

import argparse

import cv2
from src.advice_steps import AdviceSteps
from src.annotator import Annotator
from src.audio import Audio
from src.display import Display
from src.movement_extractor import MovementExtractor
from src.util import logging_basic_config


def main():
    args = run_argument_parser()

    logging_basic_config(args.log_level)

    movement = MovementExtractor.get_movement(args.movement)
    annotator = Annotator(movement)
    audio = Audio()
    display = Display('AI Coach')

    capture_input = args.video_file
    if not capture_input:
        # live capture from camera 0
        capture_input = 0
    cap = cv2.VideoCapture(capture_input)
    feedback = AdviceSteps.GET_IN_FRAME.value.title
    target = args.target \
        if args.target is not None \
        else movement['default_target']
    print(f'Using {movement["name"]} movement, target: {target}')
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            prior_feedback = feedback
            result = annotator.annotate_frame(frame)
            feedback = result.feedback

            display.display_result(result)

            audio.play_sound_if_applicable(
                result.count, target, result.feedback, prior_feedback)

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
        '--movement', '-m', help='Movement name', default='Push-up',
        choices=MovementExtractor.get_list_of_movements())
    parser.add_argument(
        '--video-file', help='File with video of exercise (example: file.mp4)')
    parser.add_argument(
        '--target', '-t',
        help='The number of reps you would like to complete (example: 20)'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
