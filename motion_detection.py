import cv2
import os

import numpy as np

def motion_detect(vid):
    edges_frames_dir = f'edges_{vid}'

    frame_files = sorted(os.listdir(edges_frames_dir))

    previous_frame = None
    total=0
    amt=0
    for i, frame_file in enumerate(frame_files):
        frame_path = os.path.join(edges_frames_dir, frame_file)

        current_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

        if current_frame is not None and previous_frame is not None:
            frame_diff = cv2.absdiff(current_frame, previous_frame)

            #threshold the difference to get a binary image of the motion
            _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

            #percentage of image that has changed
            motion_percentage = (np.sum(thresh) / thresh.size) / 255.0 * 100

            total=total+motion_percentage
            amt=amt+1
        previous_frame = current_frame
    print(f"avg={total/amt}")
def motion_detect_2(vid):
    edges_frames_dir = f'edges_{vid}'
    frame_files = sorted(os.listdir(edges_frames_dir))

    previous_frame = None

    for i, frame_file in enumerate(frame_files[:-1]):
        frame_path = os.path.join(edges_frames_dir, frame_file)
        next_frame_path = os.path.join(edges_frames_dir, frame_files[i + 1])

        current_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
        next_frame = cv2.imread(next_frame_path, cv2.IMREAD_GRAYSCALE)

        if current_frame is not None and next_frame is not None:
            frame_diff = cv2.absdiff(current_frame, next_frame)
            _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

            #morphological operations to enhance motion areas
            kernel = np.ones((5, 5), np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=1)

            #contours to detect continuous motion areas
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # threshold area
                    motion_detected = True
                    cv2.drawContours(current_frame, [contour], -1, (0, 255, 0), 2)

            cv2.imwrite(f"motion_frames_{vid}/motion_frame_{i:04d}.jpg", current_frame)
