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

## Regenerate requirements.txt

```
pip-compile
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
