import logging
import os

from gtts import gTTS
from playsound import playsound

logger = logging.getLogger(__name__)


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def _audio_full_path(path):
    """Make full path used to store audio"""
    return os.path.join(_THIS_DIR, "../audio", path)


def play_audio_file(path: str, block=False):
    """Play audio file given by path."""
    if not os.path.isabs(path):
        path = _audio_full_path(path)
    playsound(path, block)
    logger.debug(f"Play audio {path}")


def generate_audio_file(text: str):
    """Generate audio file of 'text', return path to file.

    If file already exists, just use it."""
    path = f"generated/{text}.mp3"
    fullpath = _audio_full_path(path)
    if not os.path.exists(fullpath):
        # generate audio
        tts = gTTS(text, lang="en", slow=False)
        tts.save(fullpath)
    return fullpath


def play_text(text: str, block=False):
    """Play given audio.  Generate a file on disk first, if need be."""
    play_audio_file(generate_audio_file(text), block)
