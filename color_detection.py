import cv2
import numpy as np
import os

# input_dir = 'frames_fire1'  # Directory where the frames are stored
# output_dir = 'fire_only_frames_fire1'  # Directory to save the output frames
def color(vid):
    input_dir = f'blurred_frames/blurred_frames_{vid}'
    output_dir = f'fire_only_frames/fire_only_frames_{vid}'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    list_frames = os.listdir(input_dir)


    for frame_file in os.listdir(input_dir):
    # frame_file=list_frames[0]
        frame_path = os.path.join(input_dir, frame_file)
        image = cv2.imread(frame_path)

        if image is not None:

            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            lower_bound = np.array([0, 115, 50])
            upper_bound = np.array([30, 255, 255])

            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
            fire_only = cv2.bitwise_and(image, image, mask=mask)
            output_frame_path = os.path.join(output_dir, frame_file)
            cv2.imwrite(output_frame_path, fire_only)
def color_plus_blob(vid):
    import cv2
    import numpy as np
    import os
    input_dir = f'blurred_frames/blurred_frames_{vid}'  #where the frames are stored
    output_dir = f'fire_only_frames_blob/fire_only_frames_blob_{vid}'  #save the output frames

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    list_frames = os.listdir(input_dir)

    for frame_file in os.listdir(input_dir):
    # frame_file=list_frames[0]
        frame_path = os.path.join(input_dir, frame_file)
        image = cv2.imread(frame_path)

        if image is not None:
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            lower_bound = np.array([0, 115, 70])
            upper_bound = np.array([30, 255, 255])

            mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            large_contours = [contour for contour in contours if cv2.contourArea(contour) > 700] #the threshold area is 700

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

def percentage(vid):
    input_dir = f'fire_only_frames_blob/fire_only_frames_blob_{vid}'  #where the frames are stored
    list_frames = os.listdir(input_dir)
    total=0
    num=0

    for frame_file in os.listdir(input_dir):
    # frame_file=list_frames[0]
        frame_path = os.path.join(input_dir, frame_file)
        image = cv2.imread(frame_path)
        #make gray
        if len(image.shape) == 3:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = image

        _, binary_mask = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)
        non_black_pixels = cv2.countNonZero(binary_mask)

        #number of pixels
        total_pixels = image.shape[0] * image.shape[1]

        #percentage of non-black pixels
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