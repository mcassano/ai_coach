import cv2
import numpy as np
from pose import PoseDetector
from audio import Audio
from annotator import Annotator
from gtts import gTTS
import json
import sys

def main():
    cap = cv2.VideoCapture(0)
    annotator = Annotator()
    audio = Audio()

    movement = get_desired_movement()

    count = 0.0
    direction = 0
    form = 0
    feedback = "Fix Form"
    per = 0
    target = 20
    detector = PoseDetector()
    while cap.isOpened():
        ret, frame = cap.read() #640 x 480
        #Determine dimensions of video - Help with creation of box in Line 43
        width  = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        success = False
        prior_feedback = feedback
        frame, feedback, count, per, direction, bar, success = annotator.annotateFrameWithDetector(frame, detector)

        display_result(count, form, feedback, per, frame, bar)
        
        audio.playSoundIfApplicable(count, target, feedback, prior_feedback)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def get_desired_movement():
    movements = read_movements('movements.json')

    movement_name = get_desired_movement_name_from_sys_argv()

    movement = None
    for each_movement in movements:
        if each_movement["name"] == movement_name:
            movement = each_movement
            break

    if movement == None:
        sys.exit("Movement '%s' not found in movements.json" % (movement_name))

    return movement

def get_desired_movement_name_from_sys_argv():
    movement_name = None
    try:
        movement_name = sys.argv[1]
    except IndexError:
        movement_name = "Push-up"
    return movement_name

def read_movements(path):
    f = open(path)
    movements = json.load(f)
    return movements

def display_result(count, form, feedback, per, frame, bar):
    #Draw Bar
    if form == 1:
        cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
        cv2.rectangle(frame, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)

    #Pushup counter
    cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

    #Feedback
    cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

    cv2.imshow('AI Coach', frame)

if __name__ == "__main__":
    main()
