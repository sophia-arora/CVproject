import cv2
import numpy as np
import os

# input_dir = 'frames_fire1'  # Directory where the frames are stored
# output_dir = 'fire_only_frames_fire1'  # Directory to save the output frames
def color(vid):
    input_dir = f'blurred_frames/blurred_frames_{vid}'  # Directory where the frames are stored
    output_dir = f'fire_only_frames/fire_only_frames_{vid}'  # Directory to save the output frames
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
            lower_bound = np.array([0, 115, 50])  # Adjusted lower bound of HSV for fire colors
            upper_bound = np.array([30, 255, 255])  # Adjusted upper bound of HSV for fire colors

            # Create a mask that only includes colors within the specified range
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

            # Apply the mask to get the fire parts of the image
            fire_only = cv2.bitwise_and(image, image, mask=mask)

            # Save or display the image
            output_frame_path = os.path.join(output_dir, frame_file)
            cv2.imwrite(output_frame_path, fire_only)
def color_plus_blob(vid):
    import cv2
    import numpy as np
    import os
    input_dir = f'blurred_frames/blurred_frames_{vid}'  # Directory where the frames are stored
    output_dir = f'fire_only_frames_blob/fire_only_frames_blob_{vid}'  # Directory to save the output frames
    # Ensure the output directory exists

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
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            lower_bound = np.array([0, 115, 70])  # Adjusted lower bound of HSV for fire colors
            upper_bound = np.array([30, 255, 255])  # Adjusted upper bound of HSV for fire colors

            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            large_contours = [contour for contour in contours if cv2.contourArea(contour) > 700]  # Threshold area

            large_blob_mask = np.zeros_like(mask)
            cv2.drawContours(large_blob_mask, large_contours, -1, (255), thickness=cv2.FILLED)

            fire_only = cv2.bitwise_and(image, image, mask=large_blob_mask)
            output_frame_path = os.path.join(output_dir, frame_file)
            cv2.imwrite(output_frame_path, fire_only)
def detect_fire(vid):
    input_dir = f'blurred_frames/blurred_frames_{vid}'
    output_dir = f'fire_only_frames_blob/fire_only_frames_blob_{vid}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    list_frames = os.listdir(input_dir)
    fire_contours_dict = {}

    for frame_file in os.listdir(input_dir):
        frame_path = os.path.join(input_dir, frame_file)
        image = cv2.imread(frame_path)
        fire_contours = []

        if image is not None:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower_bound = np.array([0, 115, 70])
            upper_bound = np.array([30, 255, 255])
            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            large_contours = [contour for contour in contours if cv2.contourArea(contour) > 700]

            large_blob_mask = np.zeros_like(mask)
            cv2.drawContours(large_blob_mask, large_contours, -1, (255), thickness=cv2.FILLED)

            fire_only = cv2.bitwise_and(image, image, mask=large_blob_mask)
            output_frame_path = os.path.join(output_dir, frame_file)
            cv2.imwrite(output_frame_path, fire_only)

            fire_contours.extend(large_contours)

        fire_contours_dict[frame_file] = fire_contours
    decision = percentage(vid)
    return fire_contours_dict, decision
def blur():
    # blurring
    frames_dir = f'fire_only_frames_city'
    blurred_frames_dir = f'fire_only_frames_city'
    list_frames = os.listdir(frames_dir)
    # Iterate over each file in the directory
    # for frame in os.listdir(frames_dir):
    # Construct the full file path
    frame = list_frames[0]
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

def percentage(vid):
    input_dir = f'fire_only_frames_blob/fire_only_frames_blob_{vid}'  # Directory where the frames are stored
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

            # Create a binary mask where non-black pixels are white
        _, binary_mask = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)

        # Count non-zero (non-black) pixels
        non_black_pixels = cv2.countNonZero(binary_mask)

        # Total number of pixels
        total_pixels = image.shape[0] * image.shape[1]

        # Calculate the percentage of non-black pixels
        percentage_non_black = (non_black_pixels / total_pixels) * 100
        # print(percentage_non_black)
        total=total+percentage_non_black
        num=num+1
        # return percentage_non_black
    print(f"Average: {total/num}")
    if total/num<1 :
        print(f"No fire")
        return 0
    else:
        print("fire")
        return 1
# percentage()
# color()