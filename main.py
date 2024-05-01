import cv2
import os
import track_shape
import numpy as np
import sys
import color_detection


import motion_detection
import read_video

# edge_detect()
def main(video_name):
    video_path = f"videos/{video_name}.mp4"

    if not os.path.exists(video_path):
        print(f"Error: Put your video titled {video_name} in the videos folder.")
        return
    print(video_name)
    # read_video.get_frames(video_name)
    # read_video.blur_frames(video_name)
    # read_video.edge_detect(video_name)
    # track_shape.check_shape(video_name)
    # track_shape.visualize_change(video_name)
    color_detection.color_plus_blob(video_name)
    color_detection.percentage(video_name)



# total=total/amt
# motion_detection.motion_detect("walking")
# track_shape.visualize_change("fire_only_frames_city")
# track_shape.check_shape("fire_only_frames_city")
# motion_detection.motion_detect_2("city")
# print(f"Average = {total}")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("include video name")
    else:
        main(sys.argv[1])