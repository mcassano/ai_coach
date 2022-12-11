from dataclasses import dataclass

import numpy as np


@dataclass
class AnnotationResult:
    frame: np.ndarray
    feedback: str
    count: float
    count_changed: bool
    per: float
    direction: int
    form: bool
    success: bool
    angles: dict
