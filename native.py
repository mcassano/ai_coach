import cv2
import numpy as np
from pose import PoseDetector
from annotator import Annotator
from playsound import playsound
import time
from gtts import gTTS
import os
import json
import sys

def main():
    cap = cv2.VideoCapture(0)
    annotator = Annotator()
    movement = get_desired_movement()

    count = 0.0
    direction = 0
    form = 0
    feedback = "Fix Form"
    per = 0
    target = 20
    detector = PoseDetector()
    timeSinceLastAudio = time.time()
    while cap.isOpened():
        ret, frame = cap.read() #640 x 480
        #Determine dimensions of video - Help with creation of box in Line 43
        width  = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        success = False
        prior_feedback = feedback
        frame, feedback, count, per, direction, bar, success = annotator.annotateFrameWithDetector(frame, detector)

        display_result(count, form, feedback, per, frame, bar)
        
        timeSinceLastAudio = playSoundIfApplicable(count, target, feedback, prior_feedback, timeSinceLastAudio)
    
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

def playSoundIfApplicable(count, target, feedback, prior_feedback, timeSinceLastAudio):
    # Fix form but only after 5 seconds so that you don't get hammered over and over
    if feedback == "Fix Form" and time.time() - timeSinceLastAudio > 5:
        playsound('./audio/fix_form.mp3')
        timeSinceLastAudio = time.time()
    # Was going down and now go up
    elif prior_feedback == "Down" and feedback == "Up":
        playsound('./audio/up.mp3')
        timeSinceLastAudio = time.time()
    # Was coming up and completed a rep
    elif prior_feedback == "Up" and feedback == "Down":
        if count == target:
            playsound('./audio/done.mp3')
        # Give specific count every quarter of target
        elif count % (target / 4) == 0:
            path = "./audio/count/%d.mp3" % (count)
            if not os.path.exists(path):
                tts = gTTS(text="%d" % (count), lang='en', slow=False)
                tts.save(path)
            playsound(path)
        else:
            playsound('./audio/good.mp3')
        timeSinceLastAudio = time.time()
    # Fixed form
    elif prior_feedback == "Fix Form" and feedback == "Down":
        playsound('./audio/good.mp3')
        timeSinceLastAudio = time.time()
    return timeSinceLastAudio

if __name__ == "__main__":
    main()
