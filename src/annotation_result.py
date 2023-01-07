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
    success: bool
    angles: dict
