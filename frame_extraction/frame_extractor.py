#!/usr/bin/env python

import argparse
import os
from pathlib import PurePath

import cv2
import readchar

DATA_DIR = 'data'


def main():
    # Adapted from
    # https://www.geeksforgeeks.org/extract-images-from-video-in-python/

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--video-file',
        help='File with video of frames to label (example: file.mp4)',
        required=True)
    args = parser.parse_args()

    # Read the video from specified path
    cam = cv2.VideoCapture(args.video_file)
    stem = PurePath(args.video_file).stem

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # frame
    current_frame = 0
    current_label = 'none'
    while True:
        ret, frame = cam.read()

        if ret:
            rgb_img = cv2.cvtColor(frame[:, :, ::-1], cv2.COLOR_BGR2RGB)
            cv2.imshow('frame', rgb_img)
            # image doesn't show up without waitKey
            cv2.waitKey(1)
            # but I want the character from the terminal, not the window
            key = readchar.readkey()

            if key == 's':
                # save image with label
                label = input(f'label frame {current_frame}'
                              f' (default: {current_label}): ')
                if label:
                    current_label = label

                dirname = f'{DATA_DIR}/{current_label}'
                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                name = f'{dirname}/{stem}.frame{current_frame:04d}.jpg'
                print(f'Write {name}')
                status = cv2.imwrite(name, frame)
                assert status, f"Couldn't write '{name}'"
            else:
                print(f'Skip frame {current_frame}')

            current_frame += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
