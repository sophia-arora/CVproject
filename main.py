import cv2
import os

import numpy as np


def get_frames():
    # Load the video
    video_path = 'video/fire.mp4'
    cap = cv2.VideoCapture("videos/city.mp4")

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
        frame_filename = f"frames_city/city_frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    # Release the video capture object
    cap.release()

def blur_frames():
    # Directory containing the frames
    frames_dir = 'frames_city'
    blurred_frames_dir = 'blurred_frames_city'

    # Iterate over each file in the directory
    for frame in os.listdir(frames_dir):
        # Construct the full file path
        frame_path = os.path.join(frames_dir, frame)

        # Read the image
        image = cv2.imread(frame_path)

        # Check if the image was successfully loaded
        if image is not None:
            # Apply Gaussian blur to the image
            blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

            # Construct the path for the blurred image
            blurred_frame_path = os.path.join(blurred_frames_dir, frame)

            # Save the blurred image
            cv2.imwrite(blurred_frame_path, blurred_image)
        else:
            print(f"Could not read the image {frame_path}")

def edge_detect():
    blurred_frames_dir = 'blurred_frames_city'
    edges_frames_dir = 'edges_city'


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

# edge_detect()

# Directory containing the edge-detected frames
edges_frames_dir = 'edges_city'

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

# get_frames()
# blur_frames()
# edge_detect()
total=total/amt
print(f"Average = {total}")
