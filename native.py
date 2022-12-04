# Us
import sys

# Them
import cv2

from annotator import Annotator
from audio import Audio
from display import Display
from movement_extractor import MovementExtractor
from pose import PoseDetector


def main():
    annotator = Annotator()
    audio = Audio()
    movement = MovementExtractor.get_movement(get_default_movement_name())
    display = Display('AI Coach')
    detector = PoseDetector()

    print("Using '%s' movement" % movement['name'])

    cap = cv2.VideoCapture(0)
    feedback = 'Fix Form'
    target = movement['end_at']
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            prior_feedback = feedback
            result = annotator.annotateFrameWithDetector(frame, detector)
            feedback = result.feedback

            display.display_result(result)

            audio.playSoundIfApplicable(
                result.count, target, result.feedback, prior_feedback)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    display.close()


def get_default_movement_name():
    return sys.argv[1] if len(sys.argv) >= 2 else 'Push-up'


if __name__ == '__main__':
    main()
