import cv2

import cv2
import numpy as np
import os

def visualize_overlaps(vid, overlap_frames, fire_contours_dict, motion_contours_dict):
    video_frames_dir = f'frames/frames_{vid}'
    output_frames_dir = f'visualized_overlaps/visualized_overlaps_{vid}'
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)

    for frame_file in overlap_frames.keys():
        frame_path = os.path.join(video_frames_dir, frame_file)
        original_frame = cv2.imread(frame_path)
        if original_frame is not None:
            # #draw fire contours in red
            # for contour in fire_contours_dict.get(frame_file, []):
            #     cv2.drawContours(original_frame, [contour], -1, (0, 0, 255), 2)
            #
            # #draw motion contours in blue
            # for contour in motion_contours_dict.get(frame_file, []):
            #     cv2.drawContours(original_frame, [contour], -1, (255, 0, 0), 2)

            # Draw overlap contours in green
            for (fire_contour, motion_contour) in overlap_frames[frame_file]:
                cv2.drawContours(original_frame, [fire_contour], -1, (0, 255, 0), 2)
                cv2.drawContours(original_frame, [motion_contour], -1, (0, 255, 0), 2)

            output_frame_path = os.path.join(output_frames_dir, frame_file)
            cv2.imwrite(output_frame_path, original_frame)

    print(f"Output frames with visualized overlaps have been saved in: {output_frames_dir}")


def calculate_overlap_area(fire_contour, motion_contour, image_shape):
    #blank mask for each contour
    mask_fire = np.zeros(image_shape[:2], dtype=np.uint8)
    mask_motion = np.zeros(image_shape[:2], dtype=np.uint8)

    #draw the contours on their masks
    cv2.drawContours(mask_fire, [fire_contour], -1, (255), thickness=cv2.FILLED)
    cv2.drawContours(mask_motion, [motion_contour], -1, (255), thickness=cv2.FILLED)

    #and to find overlapping area
    overlap = cv2.bitwise_and(mask_fire, mask_motion)
    #calculate the area of overlap
    overlap_area = np.count_nonzero(overlap)

    return overlap_area


def check_for_overlap(fire_contours_dict, motion_contours_dict, image_shape):
    threshold_area = 25  #overlap threshold in square pixels
    overlap_frames = {}

    for frame_file, fire_contours in fire_contours_dict.items():
        motion_contours = motion_contours_dict.get(frame_file, [])
        for fire_contour in fire_contours:
            for motion_contour in motion_contours:
                overlap_area = calculate_overlap_area(fire_contour, motion_contour, image_shape)
                if overlap_area > threshold_area:
                    if frame_file not in overlap_frames:
                        overlap_frames[frame_file] = []
                    overlap_frames[frame_file].append((fire_contour, motion_contour))

    return overlap_frames