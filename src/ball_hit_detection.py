import cv2
import numpy as np

def initialize_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to initialize webcam.")
        return None
    return cap

def detect_tennis_ball(frame):
    lower_color = np.array([25, 100, 100])
    upper_color = np.array([45, 255, 255])

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, lower_color, upper_color)

    cv2.imshow('Mask', mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def map_to_virtual_screen(x, y, frame_width, frame_height, virtual_screen_width=1920, virtual_screen_height=1080):
    scale_x = virtual_screen_width / frame_width
    scale_y = virtual_screen_height / frame_height
    return int(x * scale_x), int(y * scale_y)

def visualize_hit(virtual_screen, hit_x, hit_y):
    cv2.circle(virtual_screen, (hit_x, hit_y), 30, (0, 0, 0), -1)
    cv2.imshow('Virtual Hit Display', virtual_screen)

def main():
    cap = initialize_webcam()
    if cap is None:
        return

    frame_width, frame_height = 640, 480 
    virtual_screen_width, virtual_screen_height = 1920, 1080 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=30)

        contours = detect_tennis_ball(frame)

        for contour in contours:
            if cv2.contourArea(contour) > 500: 
                x, y, w, h = cv2.boundingRect(contour)

                hit_x, hit_y = map_to_virtual_screen(x + w // 2, y + h // 2, frame_width, frame_height, virtual_screen_width, virtual_screen_height)

                virtual_screen = np.ones((virtual_screen_height, virtual_screen_width, 3), np.uint8) * 255

                visualize_hit(virtual_screen, hit_x, hit_y)

        cv2.imshow('Webcam Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
