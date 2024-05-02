import cv2
import os

import numpy as np


def get_frames(vid):
    video_path = 'video/fire.mp4'
    cap = cv2.VideoCapture(f"videos/{vid}.mp4")
    output_dir = f'frames/frames_{vid}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not cap.isOpened():
        print("Error opening video file")

    frame_count = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame_filename = f"frames_{vid}/{vid}_frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()

def blur_frames(vid):
    frames_dir = f'frames/frames_{vid}'
    blurred_frames_dir = f'blurred_frames/blurred_frames_{vid}'
    if not os.path.exists(blurred_frames_dir):
        os.makedirs(blurred_frames_dir)

    for frame in os.listdir(frames_dir):
        frame_path = os.path.join(frames_dir, frame)

        image = cv2.imread(frame_path)

        if image is not None:
            blurred_image = cv2.GaussianBlur(image, (5, 5), 5)

            blurred_frame_path = os.path.join(blurred_frames_dir, frame)

            cv2.imwrite(blurred_frame_path, blurred_image)
        else:
            print(f"Could not read the image {frame_path}")

def edge_detect(vid):
    blurred_frames_dir = f'blurred_frames/blurred_frames_{vid}'
    edges_frames_dir = f'edges/edges_{vid}'
    if not os.path.exists(edges_frames_dir):
        os.makedirs(edges_frames_dir)


    for frame in os.listdir(blurred_frames_dir):
        frame_path = os.path.join(blurred_frames_dir, frame)
        image = cv2.imread(frame_path)
        if image is not None:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)
            edges_frame_path = os.path.join(edges_frames_dir, frame)
            cv2.imwrite(edges_frame_path, edges)
        else:
            print(f"Could not read the image {frame_path}")
