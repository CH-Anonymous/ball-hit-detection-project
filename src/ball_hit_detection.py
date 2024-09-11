import cv2
import numpy as np

# Start webcam
cap = cv2.VideoCapture(0)

# Tennis ball color range in HSV
lower_color = np.array([25, 100, 100])
upper_color = np.array([45, 255, 255])

# Define virtual screen size (16:9 ratio)
virtual_screen_width = 1920
virtual_screen_height = 1080

# Additional scaling factor for the hit location
scaling_factor = 1.5  # Increase this value to enlarge the mapped position

def map_to_virtual_screen(x, y, frame_width, frame_height):
    scale_x = virtual_screen_width / frame_width
    scale_y = virtual_screen_height / frame_height

    # Apply additional scaling factor to exaggerate the hit position
    scaled_x = x * scale_x * scaling_factor
    scaled_y = y * scale_y * scaling_factor

    # Ensure the values stay within the bounds of the virtual screen
    scaled_x = min(max(int(scaled_x), 0), virtual_screen_width)
    scaled_y = min(max(int(scaled_y), 0), virtual_screen_height)

    return scaled_x, scaled_y

# Example hit mapping
frame_width, frame_height = 640, 480  # Webcam resolution

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV and detect ball
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Ignore small areas (noise)
            x, y, w, h = cv2.boundingRect(contour)

            # Map the hit location to virtual screen with scaling
            hit_x, hit_y = map_to_virtual_screen(x + w // 2, y + h // 2, frame_width, frame_height)

            # Visualize the hit on a blank virtual screen
            virtual_screen = np.ones((virtual_screen_height, virtual_screen_width, 3), np.uint8) * 255
            cv2.circle(virtual_screen, (hit_x, hit_y), 10, (0, 0, 0), -1)  # Draw a black circle for the hit

            # Display the virtual screen with hit
            cv2.imshow('Virtual Hit Display', virtual_screen)

    # Display the webcam feed
    cv2.imshow('Tennis Ball Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
