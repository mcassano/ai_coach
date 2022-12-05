#!/usr/bin/env python

# Us
import argparse
# Them
import json

import cv2
import readchar

from src.annotator import Annotator
from src.util import logging_basic_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image-file', help='Image file to annotate',
                        required=True)
    parser.add_argument(
        '--movement', '-m', help='Movement name', default='Push-up',
        choices=['Push-up'])
    parser.add_argument(
        '--show-image', help='Show the image on the screen',
        action='store_true')
    args = parser.parse_args()

    logging_basic_config()

    annotator = Annotator(args.movement)

    frame = cv2.imread(args.image_file)
    result = annotator.annotate_frame(frame)
    print(f'angles: {json.dumps(result.angles)}')

    if args.show_image:
        cv2.imshow('frame', result.frame)
        # image doesn't show up without waitKey
        cv2.waitKey(1)
        # but I want the character from the terminal, not the window
        readchar.readkey()


if __name__ == '__main__':
    main()
