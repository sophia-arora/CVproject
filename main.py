import cv2
import os
import track_shape
import numpy as np

import motion_detection
import color_detection
import read_video

# edge_detect()

# read_video.get_frames("walking")
# read_video.blur_frames("fire_only_frames_city")
# read_video.edge_detect("fire_only_frames_city")
# total=total/amt
# motion_detection.motion_detect("walking")
# color_detection.color_plus_blob("frames_city")
# color_detection.color_plus_blob("frames_fire1")
# track_shape.visualize_change("fire_only_frames_city")
# read_video.blur_frames("new_fire_param_frames_fire1")
# read_video.edge_detect("new_fire_param_frames_fire1")
# track_shape.check_shape("new_fire_param_frames_fire1")
# track_shape.visualize_change("new_fire_param_frames_fire1")
# motion_detection.motion_detect_2("city")
# print(f"Average = {total}")
# read_video.blur_frames("city")
# read_video.edge_detect("city")
# read_video.blur_frames("fire1")

def colored_percentage(vid):
    input_dir = f'output_frames/color_blob_{vid}'  # Directory where the frames are stored
    list_frames = os.listdir(input_dir)
    total=0
    num=0
    # Iterate through each file in the directory
    for frame_file in os.listdir(input_dir):
    # frame_file=list_frames[0]
        frame_path = os.path.join(input_dir, frame_file)
        image = cv2.imread(frame_path)
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image

        non_black_pixels = cv2.countNonZero(gray_image)
        total = total + non_black_pixels
        num = image.shape[0] * image.shape[1] + num
        # print(f"Total: {total}, num: {num}")
    total = (total/num)*100
    return total

# color_detection.color_plus_blob("city")
# color_detection.color_plus_blob("fire1")
# color_detection.color_plus_blob("fire2")
# color_detection.color_plus_blob("fire3")
print(f"city: {colored_percentage('city')}")
print(f"fire1: {colored_percentage('fire1')}")
print(f"fire2: {colored_percentage('fire2')}")
print(f"fire3: {colored_percentage('fire3')}")

"""
city: 0.5897994514340464
fire1: 5.512174517791055
fire2: 0.8823784722222222
fire3: 5.708285257329052
"""

print(f"Done")