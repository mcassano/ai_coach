import cv2


class Display:
    def __init__(self, display_name):
        self.display_name = display_name

    def display_result(self, annotation_result):
        count = annotation_result.count
        form = annotation_result.form
        feedback = annotation_result.feedback
        per = annotation_result.per
        frame = annotation_result.frame

        if per is None:
            # We aren't actually in an exercise
            return

        # Draw Bar
        if form:
            cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, int(380-(380*per/100))), (600, 380),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{int(per)}%', (565, 430),
                        cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)

        # Push up counter
        cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(count)), (25, 455),
                    cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)

        # Feedback
        cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

        cv2.imshow(self.display_name, frame)

    @staticmethod
    def close():
        cv2.destroyAllWindows()
