import cv2
import numpy as np
import utils.HandTrackingModule as htm
import time
import autopy

# Set up camera window dimensions and other parameters
wCam, hCam = 640, 480  # Camera resolution
frameR = 100           # Frame reduction for better control sensitivity
smoothening = 7        # Smoothening factor for mouse movement

# Variables for frame rate calculation and mouse movement
pTime = 0              # Previous time (used for frame rate calculation)
plocX, plocY = 0, 0    # Previous location of the mouse pointer
clocX, clocY = 0, 0    # Current location of the mouse pointer

# Initialize camera capture
cap = cv2.VideoCapture(0)  # Capture from the default camera (index 0)
cap.set(3, wCam)  # Set camera width
cap.set(4, hCam)  # Set camera height

# Initialize hand detector with a maximum of 1 hand to detect
detector = htm.handDetector(maxHands=1)

# Get screen size for mouse control
wScr, hScr = autopy.screen.size()

try:
    # Main loop
    while True:
        # 1. Capture frame from the camera
        success, img = cap.read()
        if not success or img is None:
            print("Failed to capture image. Skipping this frame.")
            continue

        # 2. Detect hand and landmarks
        img = detector.findHands(img)  # Draw hand landmarks
        lmList, bbox = detector.findPosition(img)  # Get list of landmarks and bounding box

        # 3. Check if landmarks were detected (i.e., hand is in frame)
        if len(lmList) != 0:
            # Get coordinates of index (8) and middle (12) fingers
            x1, y1 = lmList[8][1:]  # Index finger tip
            x2, y2 = lmList[12][1:] # Middle finger tip

            # 4. Check which fingers are up
            fingers = detector.fingersUp()  # Returns a list of which fingers are up

            # Draw a boundary box to limit hand movement for smoother control
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

            # 5. Moving Mode: If only the index finger is up
            if fingers[1] == 1 and fingers[2] == 0:
                # 6. Convert hand coordinates to screen coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))  # Interpolate x-coordinates
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))  # Interpolate y-coordinates

                # 7. Smoothen the movement to avoid sudden jumps
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                # 8. Move the mouse to the new coordinates
                autopy.mouse.move(wScr - clocX, clocY)  # Note: wScr - clocX is used to invert the x-axis
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # Draw a circle at the index finger tip

                # Update previous locations
                plocX, plocY = clocX, clocY

            # 9. Clicking Mode: If both index and middle fingers are up
            if fingers[1] == 1 and fingers[2] == 1:
                # 10. Measure distance between index (8) and middle (12) fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)

                # 11. Perform click if the fingers are close enough (distance < 40 pixels)
                if length < 40:
                    # Draw a circle at the click position
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()  # Perform the mouse click

        # 12. Calculate and display frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Display the FPS on the image
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # 13. Show the image
        cv2.imshow("Image", img)

        # 14. Break loop on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Release the capture and destroy windows after loop ends
    cap.release()
    cv2.destroyAllWindows()
