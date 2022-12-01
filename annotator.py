import numpy as np
from pose import PoseDetector

class Annotator():
    def annotateFrameWithDetector(self, frame):
        detector = PoseDetector()

        # This was copied from https://github.com/terminalai/PushUpCounter
        frame = detector.findPose(frame, False)
        lmList = detector.findPosition(frame, False)
        feedback = ""
        recordedCount = 0
        form = 0
        count = 0
        per = 0
        direction = 0
        if len(lmList) != 0:
            elbow = detector.findAngle(frame, 11, 13, 15)
            shoulder = detector.findAngle(frame, 13, 11, 23)
            hip = detector.findAngle(frame, 11, 23,25)

            #Percentage of success of pushup
            per = np.interp(elbow, (90, 160), (0, 100))

            #Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            #Check to ensure right form before starting the program
            if elbow > 160 and shoulder > 40 and hip > 160:
                form = 1

            #Check for full range of motion for the pushup
            if form == 1:
                if per == 0:
                    if elbow <= 90 and hip > 160:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = "Fix Form"
                if per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = "Fix Form"

            recordedCount = count
        else:
            return None, None, None, None, False

        return frame, feedback, recordedCount, per, True
