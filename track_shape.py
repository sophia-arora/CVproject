import cv2
import os
import numpy as np

def check_shape(vid):
    edges_frames_dir = f'output_frames/{vid}'
    frame_files = sorted(os.listdir(edges_frames_dir))

    previous_contours = None
    significant_change_count = 0  # Counter for frames with significant shape changes
    count=0

    for i, frame_file in enumerate(frame_files[:-1]):
        frame_path = os.path.join(edges_frames_dir, frame_file)
        current_frame = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)

        if current_frame is not None:
            _, thresh = cv2.threshold(current_frame, 25, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            shape_change_detected = False
            amt = 0
            cont = 0
            if previous_contours is not None and contours:

                for contour in contours:

                    closest_contour = min(previous_contours, key=lambda x: cv2.matchShapes(x, contour, 1, 0.0))
                    shape_similarity = cv2.matchShapes(closest_contour, contour, 1, 0.0)
                    # print(f"{count}:{shape_similarity}")
                    # Assuming significant shape change if similarity is above a threshold (e.g., 0.3)
                    if shape_similarity > 2:
                        shape_change_detected = True
                        cont=cont+1
                        # Exit the loop after the first significant change detected
                    amt = amt + 1

            if amt!=0:
                if (cont/amt)>0.2:
                    significant_change_count += 1
            count=count+1
            previous_contours = contours

    print(f"Total number of frames with significant shape change: {significant_change_count}")

def visualize_change(vid):

    edges_frames_dir = f'output_frames/edges_{vid}'
    output_frames_dir = f'output_frames/change_{vid}'

    # Ensure the output directory exists
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)

    frame_files = sorted(os.listdir(edges_frames_dir))
    previous_contours = None

    for i, frame_file in enumerate(frame_files[:-1]):
        frame_path = os.path.join(edges_frames_dir, frame_file)
        current_frame = cv2.imread(frame_path)
        current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY) if current_frame is not None else None

        if current_frame_gray is not None:
            _, thresh = cv2.threshold(current_frame_gray, 25, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if previous_contours is not None and contours:
                for contour in contours:
                    closest_contour = min(previous_contours, key=lambda x: cv2.matchShapes(x, contour, 1, 0.0))
                    shape_similarity = cv2.matchShapes(closest_contour, contour, 1, 0.0)

                    if shape_similarity > 0.3:  # Threshold for significant shape change
                        # Draw the contour on the frame to highlight the change
                        cv2.drawContours(current_frame, [contour], -1, (0, 0, 255), 2)

            previous_contours = contours

            # Save the frame with the highlighted changes
            output_frame_path = os.path.join(output_frames_dir, f"changed_{frame_file}")
            cv2.imwrite(output_frame_path, current_frame)