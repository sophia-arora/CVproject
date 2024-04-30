import cv2
import os
import track_shape
import numpy as np

import motion_detection
import color_detection
import read_video

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

# read_video.blur_frames("city")
# read_video.blur_frames("fire1")
# read_video.blur_frames("fire2")
# read_video.blur_frames("fire3")

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