import cv2
import numpy as np
from pose import PoseDetector
from annotator import Annotator
from playsound import playsound
import time

def main():
    cap = cv2.VideoCapture(0)
    annotator = Annotator()

    count = 0.0
    direction = 0
    form = 0
    feedback = "Fix Form"
    recordedCount = 0
    per = 0
    detector = PoseDetector()
    timeSinceLastAudio = time.time()
    while cap.isOpened():
        ret, frame = cap.read() #640 x 480
        #Determine dimensions of video - Help with creation of box in Line 43
        width  = cap.get(3)  # float `width`
        height = cap.get(4)  # float `height`
        # print(width, height)
        success = False
        old_feedback = feedback
        frame, feedback, count, per, direction, bar, success = annotator.annotateFrameWithDetector(frame, detector)

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

        cv2.imshow('Pushup counter', frame)
        
        if feedback == "Fix Form" and time.time() - timeSinceLastAudio > 5:
            playsound('./audio/fix_form.wav')
            timeSinceLastAudio = time.time()
        elif old_feedback == "Down" and feedback == "Up":
            playsound('./audio/up.wav')
            timeSinceLastAudio = time.time()
        elif old_feedback == "Up" and feedback == "Down":
            playsound('./audio/good.wav')
            timeSinceLastAudio = time.time()
        elif old_feedback == "Fix Form" and feedback == "Down":
            playsound('./audio/good.wav')
            timeSinceLastAudio = time.time()
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
