import cv2
import numpy as np

# 1. Webcam Setup
def initialize_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to initialize webcam.")
        return None
    return cap

# 2. Tennis Ball Detection Using Color Filtering
def detect_tennis_ball(frame):
    # Tennis ball color range in HSV (adjust as needed)
    lower_color = np.array([25, 100, 100])
    upper_color = np.array([45, 255, 255])

    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to filter the color
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Show mask for debugging
    cv2.imshow('Mask', mask)

    # Find contours of the detected ball
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# 3. Mapping the Hit to the Virtual Screen
def map_to_virtual_screen(x, y, frame_width, frame_height, virtual_screen_width=1920, virtual_screen_height=1080):
    scale_x = virtual_screen_width / frame_width
    scale_y = virtual_screen_height / frame_height
    return int(x * scale_x), int(y * scale_y)

# 4. Visualizing the Hit on the Virtual Screen
def visualize_hit(virtual_screen, hit_x, hit_y):
    cv2.circle(virtual_screen, (hit_x, hit_y), 30, (0, 0, 0), -1)  # Increased circle radius to 30 for larger spot
    cv2.imshow('Virtual Hit Display', virtual_screen)

# 5. Main Logic for Detecting Hits and Mapping to Virtual Screen
def main():
    cap = initialize_webcam()
    if cap is None:
        return

    frame_width, frame_height = 640, 480  # Webcam resolution
    virtual_screen_width, virtual_screen_height = 1920, 1080  # Virtual screen size (16:9 ratio)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Optional: Adjust brightness/contrast for better visibility
        frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=30)

        contours = detect_tennis_ball(frame)  # Detect tennis ball

        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Adjust contour area if necessary
                x, y, w, h = cv2.boundingRect(contour)

                # Map hit location to virtual screen
                hit_x, hit_y = map_to_virtual_screen(x + w // 2, y + h // 2, frame_width, frame_height, virtual_screen_width, virtual_screen_height)

                # Create a blank virtual screen
                virtual_screen = np.ones((virtual_screen_height, virtual_screen_width, 3), np.uint8) * 255

                # Visualize hit on virtual screen
                visualize_hit(virtual_screen, hit_x, hit_y)

        # Display the webcam feed
        cv2.imshow('Webcam Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# Execute the main function
if __name__ == "__main__":
    main()
