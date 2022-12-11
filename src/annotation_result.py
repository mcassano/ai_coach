from dataclasses import dataclass

import numpy as np


@dataclass
class AnnotationResult:
    frame: np.ndarray
    feedback: str
    count: float
    rep_completed: bool
    per: float
    direction: int
    form: bool
    success: bool
    angles: dict
