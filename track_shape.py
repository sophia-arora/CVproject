import cv2
import os
import numpy as np

def check_shape(vid):
    edges_frames_dir = f'edges_{vid}'
    frame_files = sorted(os.listdir(edges_frames_dir))

    previous_contours = None
    significant_change_count = 0  # Counter for frames with significant shape changes

    for i, frame_file in enumerate(frame_files[:-1]):
        frame_path = os.path.join(edges_frames_dir, frame_file)
        current_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

        if current_frame is not None:
            _, thresh = cv2.threshold(current_frame, 25, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            shape_change_detected = False
            if previous_contours is not None and contours:
                for contour in contours:
                    closest_contour = min(previous_contours, key=lambda x: cv2.matchShapes(x, contour, 1, 0.0))
                    shape_similarity = cv2.matchShapes(closest_contour, contour, 1, 0.0)

                    # Assuming significant shape change if similarity is above a threshold (e.g., 0.3)
                    if shape_similarity > 0.3:
                        shape_change_detected = True
                        break  # Exit the loop after the first significant change detected

            if shape_change_detected:
                significant_change_count += 1

            previous_contours = contours

    print(f"Total number of frames with significant shape change: {significant_change_count}")