# Hand Gestures Live Mouse Control

Control your mouse using hand gestures detected from your webcam using OpenCV and MediaPipe.

## Requirements

- Python 3.12 (recommended)
- Webcam
- Windows (tested)

## Install

```
py -3.12 -m pip install -r requirements.txt
```

## Run

```
A window "Hand Gesture Mouse Control" opens. Press `q` to quit.
py -3.12 main.py
```

A window "Hand Gesture Mouse Control" opens. Press `q` to quit.

## Gestures

- Move mouse: Thumb–index close (< ~50 px), index extended
- Left click: Index bent, middle straight, thumb away
- Right click: Middle bent, index straight, thumb away
- Double click: Both index and middle bent, thumb away
- Screenshot: Both index and middle bent, thumb close

## Troubleshooting

- If MediaPipe errors, ensure mediapipe>=0.10.13 is installed.
- If webcam not found, check `cv2.VideoCapture(0)` and camera permissions.
