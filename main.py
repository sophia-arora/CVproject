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
color_detection.color_plus_blob("frames_city")
# track_shape.visualize_change("fire_only_frames_city")
# track_shape.check_shape("fire_only_frames_city")
# motion_detection.motion_detect_2("city")
# print(f"Average = {total}")
