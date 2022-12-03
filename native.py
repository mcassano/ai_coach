import cv2
import numpy as np
from pose import PoseDetector
from annotator import Annotator
from playsound import playsound
import time
from gtts import gTTS
import os

def main():
    cap = cv2.VideoCapture(0)
    annotator = Annotator()

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
        playsound('./audio/fix_form.wav')
        timeSinceLastAudio = time.time()
    # Was going down and now go up
    elif prior_feedback == "Down" and feedback == "Up":
        playsound('./audio/up.wav')
        timeSinceLastAudio = time.time()
    # Was coming up and completed a rep
    elif prior_feedback == "Up" and feedback == "Down":
        if count == target:
            playsound('./audio/done.wav')
        elif count % 5 == 0:
            path = "./audio/count/%d.wav" % (count)
            if not os.path.exists(path):
                tts = gTTS(text="%d" % (count), lang='en', slow=False)
                    # Saving the converted audio in a wav file named sample
                tts.save(path)
            playsound(path)
        else:
            playsound('./audio/good.wav')
        timeSinceLastAudio = time.time()
    # Fixed form
    elif prior_feedback == "Fix Form" and feedback == "Down":
        playsound('./audio/good.wav')
        timeSinceLastAudio = time.time()
    return timeSinceLastAudio

if __name__ == "__main__":
    main()
