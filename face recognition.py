import cv2
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open a connection to the camera
cap = cv2.VideoCapture(0)

# Initialize previous hand position
prev_hand_pos = None

# Get the default audio endpoint for playback devices
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        # Extract hand landmarks
        landmarks = results.multi_hand_landmarks[0].landmark

        # Get the position of the thumb (assuming right hand)
        thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]

        # Convert thumb tip coordinates to screen coordinates
        thumb_x = int(thumb_tip.x * frame.shape[1])
        thumb_y = int(thumb_tip.y * frame.shape[0])

        # Draw a circle at the thumb tip position
        cv2.circle(frame, (thumb_x, thumb_y), 15, (0, 255, 0), -1)

        # Adjust volume based on thumb vertical position
        if prev_hand_pos:
            delta_y = thumb_y - prev_hand_pos[1]
            volume_change = int(delta_y / 10)  # Adjust sensitivity by changing the divisor
            current_volume = volume.GetMasterVolumeLevelScalar()
            new_volume = np.clip(current_volume + volume_change / 100.0, 0.0, 1.0)
            volume.SetMasterVolumeLevelScalar(new_volume, None)

        # Update previous hand position
        prev_hand_pos = (thumb_x, thumb_y)

    # Display the frame
    cv2.imshow('Volume Control', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
