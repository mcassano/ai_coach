#!/usr/bin/env python

import os

import cv2
import readchar


def main():
    # Adapted from
    # https://www.geeksforgeeks.org/extract-images-from-video-in-python/

    # Read the video from specified path
    the_file = 'tmp/the-perfect-push-up-do-it-right.mp4'
    cam = cv2.VideoCapture(the_file)

    if not os.path.exists('data'):
        os.makedirs('data')

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
                name = f'./data/{current_label}.{current_frame:04d}.jpg'
                print(f'Write {name}')
                cv2.imwrite(name, frame)
            else:
                print(f'Skip frame {current_frame}')

            current_frame += 1
        else:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
