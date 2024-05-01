import cv2
import os

import numpy as np


def get_frames(vid):
    # Load the video
    video_path = 'video/fire.mp4'
    cap = cv2.VideoCapture(f"videos/{vid}.mp4")
    output_dir = f'frames/frames_{vid}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Check if video opened successfully
    if not cap.isOpened():
        print("Error opening video file")

    frame_count = 0
    while True:
        # Read the next frame
        ret, frame = cap.read()

        # If frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Save the frame as a JPEG file
        frame_filename = f"frames_{vid}/{vid}_frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    # Release the video capture object
    cap.release()

def blur_frames(vid):
    # Directory containing the frames
    frames_dir = f'frames/frames_{vid}'
    blurred_frames_dir = f'blurred_frames/blurred_frames_{vid}'
    if not os.path.exists(blurred_frames_dir):
        os.makedirs(blurred_frames_dir)

    # Iterate over each file in the directory
    for frame in os.listdir(frames_dir):
        # Construct the full file path
        frame_path = os.path.join(frames_dir, frame)

        # Read the image
        image = cv2.imread(frame_path)

        # Check if the image was successfully loaded
        if image is not None:
            # Apply Gaussian blur to the image
            blurred_image = cv2.GaussianBlur(image, (5, 5), 5)

            # Construct the path for the blurred image
            blurred_frame_path = os.path.join(blurred_frames_dir, frame)

            # Save the blurred image
            cv2.imwrite(blurred_frame_path, blurred_image)
        else:
            print(f"Could not read the image {frame_path}")

def edge_detect(vid):
    blurred_frames_dir = f'blurred_frames/blurred_frames_{vid}'
    edges_frames_dir = f'edges/edges_{vid}'
    if not os.path.exists(edges_frames_dir):
        os.makedirs(edges_frames_dir)


    # Iterate over each file in the blurred frames directory
    for frame in os.listdir(blurred_frames_dir):
        # Construct the full file path
        frame_path = os.path.join(blurred_frames_dir, frame)

        # Read the image
        image = cv2.imread(frame_path)

        # Check if the image was successfully loaded
        if image is not None:
            # Convert the image to grayscale
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply Canny edge detection
            edges = cv2.Canny(gray_image, threshold1=50, threshold2=150)

            # Construct the path for the edge-detected image
            edges_frame_path = os.path.join(edges_frames_dir, frame)

            # Save the edge-detected image
            cv2.imwrite(edges_frame_path, edges)
        else:
            print(f"Could not read the image {frame_path}")
