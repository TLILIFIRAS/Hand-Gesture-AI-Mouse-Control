# Hand-Gesture-AI-Mouse-Control
This project allows you to control your computer's mouse using hand gestures captured by a webcam. The system uses a combination of OpenCV, MediaPipe (via a custom Hand Tracking Module), and Autopy to track hand movements and perform actions like moving the mouse pointer and clicking, based on specific gestures.

# Hand Gesture Mouse Control

This project allows you to control your computer's mouse using hand gestures captured by a webcam. The system uses a combination of OpenCV, MediaPipe (via a custom Hand Tracking Module), and Autopy to track hand movements and perform actions like moving the mouse pointer and clicking, based on specific gestures.

## Features

- **Move Mouse Cursor**: Use your index finger to control the movement of the mouse cursor.
- **Left Click**: Perform a left-click by bringing your index and middle fingers close together.
- **Smooth Movement**: Mouse movement is smoothened to prevent jerky transitions.
- **Frame Reduction**: Only the area within a reduced frame is used for mouse control, giving more precise movements.

## Project Structure

```bash
.
├── utils/
│   └── HandTrackingModule.py   # Custom module for hand tracking
├── AI_Virtual_Mouse.py         # Main Python script for the project
└── README.md                   # Project documentation
```
## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.6 or above
- OpenCV (`cv2`)
- NumPy (`numpy`)
- Autopy (`autopy`)
- A webcam or camera for hand tracking

### Install Required Packages

You can install the required Python packages using `pip`:

```bash
pip install opencv-python numpy autopy mediapipe
```
### Hand Tracking Module
This project uses a custom hand tracking module (HandTrackingModule.py), which is responsible for detecting hand landmarks, identifying which fingers are up, and calculating distances between key landmarks. This module is based on MediaPipe.
HandTrackingModule.py
The HandTrackingModule.py should include the following key functions:

- findHands(img): Detects hands in the given image.
- findPosition(img): Returns a list of hand landmarks and their positions.
- fingersUp(): Identifies which fingers are up based on hand landmarks.
- findDistance(p1, p2, img): Calculates the distance between two finger landmarks.
- Make sure this module is placed inside the utils/ folder.
