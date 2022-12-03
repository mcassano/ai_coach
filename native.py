# Us
from pose import PoseDetector
from audio import Audio
from annotator import Annotator
from movement_extractor import MovementExtractor
from display import Display
from annotation_result import AnnotationResult

# Them
import cv2
import sys

def main():
    annotator = Annotator()
    audio = Audio()
    movement = MovementExtractor.get_movement(get_default_movement_name())
    display = Display('AI Coach')

    print("Using '%s' movement" % movement["name"])

    cap = cv2.VideoCapture(0)
    feedback = "Fix Form"
    target = 20
    detector = PoseDetector()
    while cap.isOpened():
        ret, frame = cap.read() #640 x 480
        #Determine dimensions of video - Help with creation of box in Line 43
        width  = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        success = False
        prior_feedback = feedback
        result = annotator.annotateFrameWithDetector(frame, detector)
        feedback = result.feedback

        display.display_result(result)
        
        audio.playSoundIfApplicable(result.count, target, result.feedback, prior_feedback)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    display.close()

def get_default_movement_name():
    return sys.argv[1] if len(sys.argv) >= 2 else 'Push-up'

if __name__ == "__main__":
    main()
