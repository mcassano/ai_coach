#!/usr/bin/env python

"""
Example usage:

$ bin/process_images.py data/pushup_up/*
$ bin/process_images.py --show tests/mike_pushup_down_small.jpg
"""

import argparse
import json

import cv2
import readchar
from src.annotator import Annotator
from src.exercise import Exercise
from src.util import logging_basic_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'imagefile', help='Image file(s) to annotate', nargs='+')
    parser.add_argument(
        '--exercise', '-e', help='Exercise name', default='Push-up',
        choices=Exercise.exercise_names())
    parser.add_argument(
        '--show-image', help='Show the image on the screen',
        action='store_true')
    args = parser.parse_args()

    logging_basic_config()

    exercise = Exercise.exercise(args.exercise)
    annotator = Annotator(
        exercise,
        # annotate images that may be completely unrelated to each other
        static_image_mode=True)

    print('[')
    idx = 0
    for image_file in args.imagefile:
        frame = cv2.imread(image_file)
        result = annotator.annotate_frame(frame)
        if idx > 0:
            print(', ', end='')
        data = {'angles': result.angles,
                'file': image_file}
        print(json.dumps(data))

        if args.show_image:
            cv2.imshow('frame', result.frame)
            # image doesn't show up without waitKey
            cv2.waitKey(1)
            # but I want the character from the terminal, not the window
            readchar.readkey()
        idx += 1
    print(']')


if __name__ == '__main__':
    main()
