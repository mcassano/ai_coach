import logging
import os


def logging_basic_config(level=None):
    """basicConfig with a standard logging format.

    If level is not given, default to env var LOG_LEVEL, or WARNING."""
    if not level:
        level = os.getenv('LOG_LEVEL', 'WARNING')
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s')
