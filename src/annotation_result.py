from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class AnnotationResult:
    frame: np.ndarray
    feedback: str
    rep_count: float
    rep_completed: bool
    per: float
    direction: int
    # the right form is being held
    right_form: bool
    # number of seconds the right form has been held
    right_form_seconds: int
    # number of seconds left to hold the right form
    seconds_left: int
    # each angle, and whether it's valid or not
    angle_validation: dict[str, bool]
    success: bool
    angles: dict
    exercise_num_steps: int
