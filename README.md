# AI Coach
Python system to coach you on push-ups, designed to be run on the Vizy platform or natively on a Macbook Pro.

## Vizy
Copy this repo into the /home/pi/vizy/apps directory and Vizy should pick it up as "AI Coach" under the "Apps" menu.

### Dependency installation on Vizy
Any or all of the following libraries might be required in order to run mediapipe on version 0.2.114 of Vizy.  We should figure out which ones are actually required.
```
sudo apt install ffmpeg python3-opencv python3-pip
sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1 libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
sudo apt-get install python-opencv
pip3 install mediapipe-rpi4
```

The pose system in mediapipe requires a TFLife model, this repo currently uses the following:
```
curl https://storage.googleapis.com/mediapipe-assets/pose_landmark_heavy.tflite --output pose_landmark_heavy.tflite
sudo mv pose_landmark_heavy.tflite /usr/local/lib/python3.7/dist-packages/mediapipe/modules/pose_landmark/
```

## Macbook Pro
Clone the repo into a directory, make a virtual environment and install from requirements.txt:
```
git clone ...
python3 -m venv my_venv
pip3 install -r requirements.txt
```

## Regenerate requirements.txt

```
pip-compile
```

# Run the application


```
python3 ./native.py
```
