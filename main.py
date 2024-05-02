import cv2
import os

import overlap
import track_shape
import numpy as np
import sys
import color_detection
import time


import motion_detection
import read_video

# edge_detect()

def play_video(video_name, folder, val):
    # Frame rate control
    vid=video_name
    video_name = f"{folder}_{video_name}"  # Replace with your actual video name
    base_dir = f"{folder}"  # The directory where your frames are stored
    val=1
    frames_path = os.path.join(base_dir, video_name)
    if not os.path.exists(frames_path):
        # print(f"no fire detected")
        video_name = f"frames_{vid}"
        base_dir= f"frames"
        frames_path = f"frames/frames_{vid}"
        if not os.path.exists(frames_path):
            print(f"Please put {vid} in the videos folder and run 'make video'")
            return
        val=0
        frame_files = sorted(os.listdir(frames_path))
    else:
        frame_files = sorted(os.listdir(frames_path))  # Ensure files are sorted correctly

    window_name = 'Video Playback'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    frame_rate = 30  # frames per second
    delay = 1 / frame_rate  # delay in seconds between frames

    for frame_file in frame_files:
        frame_path = os.path.join(frames_path, frame_file)
        frame = cv2.imread(frame_path)

        if frame is not None:
            # Create space for text by padding the frame
            padded_frame = cv2.copyMakeBorder(frame, 120, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

            # Add text to the padded frame
            if val==1:
                text = "Possible fire detected"
            else:
                text = "No Fire"
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_color = (255, 255, 255)  # White text
            cv2.putText(padded_frame, text, (50, 100), font, 3, text_color, 3)

            cv2.imshow(window_name, padded_frame)
            time.sleep(delay)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit early
                break

            # Check if the window is closed
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
        else:
            print(f"Failed to load the image from {frame_path}. Check the file path and permissions.")

    cv2.destroyAllWindows()
def make_video(video_name):
    video_path = f"videos/{video_name}.mp4"
    if not os.path.exists(video_path):
        print(f"Error: Put your video titled {video_name} in the videos folder.")
        return
    print(video_name)
    read_video.get_frames(video_name)
    read_video.blur_frames(video_name)
    read_video.edge_detect(video_name)
    list_frames = os.listdir(f"frames/frames_{video_name}")
    frame_path = list_frames[0]
    print("Attempting to load image from:", frame_path)
    image = cv2.imread(f"frames/frames_{video_name}/{frame_path}")
    # cv2.imshow('Frame', image)
    image_shape=image.shape



    fire_contours_dict, decision = color_detection.detect_fire(video_name)
    if decision == 1:
        motion_contours_dict = track_shape.detect_motion_changes(video_name)
        overlap_frames = overlap.check_for_overlap(fire_contours_dict, motion_contours_dict, image_shape)
        overlap.visualize_overlaps(video_name, overlap_frames, fire_contours_dict, motion_contours_dict)
        folder = "visualized_overlaps"
        play_video(video_name, folder, 1)
    else:
        folder = "frames"
        play_video(video_name, folder, 0)


def main(video_name):
    video_path = f"videos/{video_name}.mp4"
    folder = "visualized_overlaps"
    play_video(video_name, folder, 1)
    # make_video(video_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("include video name")
    else:
        main(sys.argv[1])