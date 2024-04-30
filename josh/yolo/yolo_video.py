import os

from ultralytics import YOLO
import cv2

input_video_path = 'videos/fire3.mp4'
output_video_path = 'videos/fire3_output.mp4'

cap = cv2.VideoCapture(input_video_path)
#ret, frame = cap.read()
#H, W, _ = frame.shape
if not cap.isOpened():
    print("Error: Could not open video file:", input_video_path)
else:
    # Try to read the first frame to confirm the video file can be read
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read the first frame from the video file")
    else:
        # Successfully read the first frame, now we can proceed
        H, W, _ = frame.shape
        print("Video opened successfully. Frame dimensions:", H, "x", W)

out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('josh', 'yolo','runs', 'detect', 'train3', 'weights', 'best.pt')

# Load a model
model = YOLO(model_path)  # load a custom model

threshold = 0.2

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab a frame or end of video reached")
        break  # Exit the loop if no frame is grabbed or end of video is reached

    H, W, _ = frame.shape  # Safe to access frame.shape because frame is not None

    # Process the frame
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame)  # Write the processed frame to the output file

# After the loop
cap.release()
out.release()
cv2.destroyAllWindows()