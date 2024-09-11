import cv2
import numpy as np

# 1. Webcam Setup
def initialize_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to initialize webcam.")
        return None
    return cap

# 2. Preprocess frame (blurring to reduce noise)
def preprocess_frame(frame):
    # Resize frame to reduce processing load
    frame = cv2.resize(frame, (640, 480))
    
    # Apply Gaussian blur to smooth the image and reduce noise
    blurred_frame = cv2.GaussianBlur(frame, (11, 11), 0)
    
    return blurred_frame

# 3. Tennis Ball Detection Using Color Filtering
def detect_tennis_ball(frame, lower_color, upper_color):
    # Convert frame to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask to filter the color
    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    # Apply a series of dilations and erosions to eliminate noise and fill gaps
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours of the detected ball
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours

# 4. Mapping the Hit to the Virtual Screen
def map_to_virtual_screen(x, y, frame_width, frame_height, virtual_screen_width=1920, virtual_screen_height=1080):
    scale_x = virtual_screen_width / frame_width
    scale_y = virtual_screen_height / frame_height
    return int(x * scale_x), int(y * scale_y)

# 5. Visualizing the Hit on the Virtual Screen
def visualize_hit(virtual_screen, hit_x, hit_y):
    cv2.circle(virtual_screen, (hit_x, hit_y), 30, (0, 0, 0), -1)  # Increased circle radius to 30 for larger spot
    cv2.imshow('Virtual Hit Display', virtual_screen)

# Helper function to display trackbars for real-time HSV adjustment
def adjust_hsv_range():
    def nothing(x):
        pass
    cv2.namedWindow('Adjust HSV')
    cv2.createTrackbar('Lower H', 'Adjust HSV', 25, 255, nothing)
    cv2.createTrackbar('Lower S', 'Adjust HSV', 100, 255, nothing)
    cv2.createTrackbar('Lower V', 'Adjust HSV', 100, 255, nothing)
    cv2.createTrackbar('Upper H', 'Adjust HSV', 45, 255, nothing)
    cv2.createTrackbar('Upper S', 'Adjust HSV', 255, 255, nothing)
    cv2.createTrackbar('Upper V', 'Adjust HSV', 255, 255, nothing)

# 6. Main Logic for Detecting Hits and Mapping to Virtual Screen
def main():
    cap = initialize_webcam()
    if cap is None:
        return

    frame_width, frame_height = 640, 480  # Webcam resolution
    virtual_screen_width, virtual_screen_height = 1920, 1080  # Virtual screen size (16:9 ratio)

    # Set up trackbars to adjust HSV range dynamically
    adjust_hsv_range()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Preprocess frame (resize, blur, etc.)
        preprocessed_frame = preprocess_frame(frame)

        # Read trackbar positions for dynamic HSV tuning
        lower_h = cv2.getTrackbarPos('Lower H', 'Adjust HSV')
        lower_s = cv2.getTrackbarPos('Lower S', 'Adjust HSV')
        lower_v = cv2.getTrackbarPos('Lower V', 'Adjust HSV')
        upper_h = cv2.getTrackbarPos('Upper H', 'Adjust HSV')
        upper_s = cv2.getTrackbarPos('Upper S', 'Adjust HSV')
        upper_v = cv2.getTrackbarPos('Upper V', 'Adjust HSV')

        # Define the lower and upper color range for tennis ball detection
        lower_color = np.array([lower_h, lower_s, lower_v])
        upper_color = np.array([upper_h, upper_s, upper_v])

        contours = detect_tennis_ball(preprocessed_frame, lower_color, upper_color)

        if contours:
            # Find the largest contour assuming it's the tennis ball
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:
                x, y, w, h = cv2.boundingRect(largest_contour)

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
