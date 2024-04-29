import cv2
import numpy as np
import os

# input_dir = 'frames_fire1'  # Directory where the frames are stored
# output_dir = 'fire_only_frames_fire1'  # Directory to save the output frames

input_dir = 'frames_city'  # Directory where the frames are stored
output_dir = 'fire_only_frames_city'  # Directory to save the output frames
# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

list_frames = os.listdir(input_dir)

# Iterate through each file in the directory
for frame_file in os.listdir(input_dir):
# frame_file=list_frames[0]
    frame_path = os.path.join(input_dir, frame_file)
    image = cv2.imread(frame_path)

    if image is not None:
        # Convert the image from BGR to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define the range of colors for fire (these values can be adjusted)
        lower_bound = np.array([0, 50, 50])  # Lower bound of HSV for fire colors
        upper_bound = np.array([50, 255, 255])  # Upper bound of HSV for fire colors

        # Create a mask that only includes colors within the specified range
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        # Apply the mask to get the fire parts of the image
        fire_only = cv2.bitwise_and(image, image, mask=mask)

        # Save or display the image
        output_frame_path = os.path.join(output_dir, frame_file)
        cv2.imwrite(output_frame_path, fire_only)