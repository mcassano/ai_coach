class AnnotationResult:
    def __init__(self, frame, feedback: str, count: float,
                 per: float, direction: int, form: bool,
                 success, angles: dict):
        self.frame = frame
        self.feedback = feedback
        self.count = count
        self.per = per
        self.direction = direction
        self.form = form
        self.success = success
        self.angles = angles
