# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



import cv2


import os
def get_frames():
    # Load the video
    video_path = 'video/fire.mp4'
    cap = cv2.VideoCapture("videos/fire1.mp4")

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
        frame_filename = f"frames_fire1/fire1_frame_{frame_count:04d}.jpg"
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    # Release the video capture object
    cap.release()

def blur_frames():


    # Directory containing the frames
    frames_dir = 'frames_fire1'
    blurred_frames_dir = 'blurred_frames_fire1'

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
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    blur_frames()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
