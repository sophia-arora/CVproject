import cv2
import os

import numpy as np

def motion_detect(vid):
    # Directory containing the edge-detected frames
    edges_frames_dir = f'edges_{vid}'

    # Get a sorted list of all frame filenames
    frame_files = sorted(os.listdir(edges_frames_dir))

    # Initialize the previous frame variable
    previous_frame = None
    total=0
    amt=0
    # Iterate over each file in the edge-detected frames directory
    for i, frame_file in enumerate(frame_files):
        # Construct the full file path
        frame_path = os.path.join(edges_frames_dir, frame_file)

        # Read the image
        current_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

        # Check if the frame was successfully loaded
        if current_frame is not None and previous_frame is not None:
            # Compute the absolute difference between the current frame and the previous frame
            frame_diff = cv2.absdiff(current_frame, previous_frame)

            # Threshold the difference to get a binary image of the motion
            _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

            # Find the percentage of image that has changed
            motion_percentage = (np.sum(thresh) / thresh.size) / 255.0 * 100

            # You can now use motion_percentage to decide if significant motion occurred
            # print(f"Frame {i}: Motion percentage = {motion_percentage:.2f}%")
            total=total+motion_percentage
            amt=amt+1
            # For visualization, you might want to save or display the thresholded difference
            # For example, to save the image uncomment the following line:
            # cv2.imwrite(f"motion_frame_{i:04d}.jpg", thresh)

        # Update the previous frame
        previous_frame = current_frame
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

            # Apply morphological operations to enhance motion areas
            kernel = np.ones((5, 5), np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=1)

            # Find contours to detect continuous motion areas
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > 100:  # threshold area
                    motion_detected = True
                    cv2.drawContours(current_frame, [contour], -1, (0, 255, 0), 2)

            # if motion_detected:
                # print(f"Motion detected in frame {i}")

            # Save or display the frame for verification
            cv2.imwrite(f"motion_frames_{vid}/motion_frame_{i:04d}.jpg", current_frame)
