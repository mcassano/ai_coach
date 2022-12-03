import numpy as np

class Annotator():
    def __init__(self):
        self.recorded_count = 0
        self.direction = 0
        self.feedback = ""
        self.form = 0
        self.per = 0

    def annotateFrameWithDetector(self, frame, detector):
        # This was copied from https://github.com/terminalai/PushUpCounter
        frame = detector.findPose(frame, False)
        lmList = detector.findPosition(frame, False)
        count = 0
        bar = 0
        if len(lmList) != 0:
            elbow = detector.findAngle(frame, 11, 13, 15)
            shoulder = detector.findAngle(frame, 13, 11, 23)
            hip = detector.findAngle(frame, 11, 23,25)

            #Percentage of success of pushup
            self.per = np.interp(elbow, (90, 160), (0, 100))

            #Bar to show Pushup progress
            bar = np.interp(elbow, (90, 160), (380, 50))

            #Check to ensure right form before starting the program
            if elbow > 160 and shoulder > 40 and hip > 160:
                self.form = 1

            #Check for full range of motion for the pushup
            if self.form == 1:
                if self.per == 0:
                    if elbow <= 90 and hip > 160:
                        self.feedback = "Up"
                        if self.direction == 0:
                            count = 0.5
                            self.direction = 1
                    else:
                        self.feedback = "Fix Form"
                if self.per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        self.feedback = "Down"
                        if self.direction == 1:
                            count = 0.5
                            self.direction = 0
                    else:
                        self.feedback = "Fix Form"
            else:
                self.feedback = "Fix Form"

            self.recorded_count = self.recorded_count + count
            return frame, self.feedback, self.recorded_count, self.per, self.direction, bar, True
        return None, "", 0, -1.0, self.direction, bar, False
