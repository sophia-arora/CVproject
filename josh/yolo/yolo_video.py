import os

from ultralytics import YOLO
import cv2

# path to media
input_video_path = 'josh/yolo/vids/housefire.mp4'
#input_video_path = 'videos/city.mp4'
output_video_path = 'josh/yolo/vids/housefire_yolov8n.mp4'

cap = cv2.VideoCapture(input_video_path)
#ret, frame = cap.read()
#H, W, _ = frame.shape
if not cap.isOpened():
    print("Error: Could not open video file:", input_video_path)
else:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read the first frame from the video file")
    else:
        H, W, _ = frame.shape
        print("Video opened successfully. Frame dimensions:", H, "x", W)

out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

#model_path = os.path.join('josh', 'yolo','runs', 'detect', 'train10', 'weights', 'best.pt')
model_path = os.path.join('josh', 'yolo','yolo_output', 'yolov8n.pt')

model = YOLO(model_path) 

threshold = 0.2

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab a frame or end of video reached")
        break  

    H, W, _ = frame.shape 

    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

    out.write(frame) 

cap.release()
out.release()
cv2.destroyAllWindows()