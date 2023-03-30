# AI Coach
Python system to coach you on push-ups, designed to be run on a Macbook Pro using python3

## Installation
Clone the repo into a directory, make a virtual environment and install from requirements.txt:
```
git clone ...
python3 -m venv my_venv
source my_venv/bin/activate
pip3 install -r requirements.txt
```

## Regenerate requirements.txt and requirements-silicon.txt
We support (at least) three platforms in requirements.in: Apple Silicon Mac, Intel Mac and Ubuntu.  requirements.in has
markers that pip-compile will pick up on to generate the lockfile.  requirements.txt is for Intel Mac and Ubuntu,
requirements-silicon.txt is for Apple Silicon Mac.

To generate requirements.txt, run from a Intel Mac or Ubuntu:
```
pip-compile
```

To generate requirements-silicon.txt, run from a Apple Silicon Mac:
```
pip-compile -o requirements-silicon.txt
```

Also install `pre-commit`:

```
brew install pre-commit
pre-commit install
pre-commit autoupdate
```

To run pre-commit on everything:

```
pre-commit run --all
```

To run the pylint check (a picky one):

```
pre-commit run --all pylint
```

# Run the application

Set PYTHONPATH.

```buildoutcfg
export PYTHONPATH=.
```

Run with default camera chosen by OpenCV:

```
./bin/coach.py
```

Run with a video file (referenced video file doesn't exist in repo):

```
./bin/coach.py --video-file ./trimmed-pushup.mp4
```

Run with a static image:

```
./bin/coach.py --video-file ./tests/mike_pushup_up_small.jpg
```

# Run the tests
```
python -m unittest discover tests
```

# Setting environment variables for posting results to ai_coach_web
```
# Get an API key from ai_coach_web
export AI_COACH_WEB_API_KEY=THE_KEY_YOU_GOT
export AI_COACH_WEB_HOSTNAME=http://localhost:8000
```
