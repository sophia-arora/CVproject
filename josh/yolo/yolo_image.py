from ultralytics import YOLO
import os

def image_detection(image_path):
    model_location = os.path.join('runs', 'detect', 'train3', 'weights', 'best.pt')
    model = YOLO(model_location)

    results = model(image_path)
    return results


def debug():
    print(os.getcwd() + "C:/Users/Joshua Huang/AppData/Local/Programs/Python")
    file_path = os.path.join('josh', 'yolo', 'runs', 'detect', 'train3', 'weights', 'best.pt')

    # Check if the file exists
    if os.path.exists(file_path):
        print("File exists.")
    else:
        print("File does not exist.")

debug()

