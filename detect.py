from ultralytics import YOLO
import cv2
import os

model = YOLO("yolov8n.pt")  # Nano model, fast and light

def detect_clothes(image_path):
    results = model(image_path)
    detections = results[0].boxes.data.cpu().numpy()

    if not os.path.exists("cropped"):
        os.makedirs("cropped")

    image = cv2.imread(image_path)
    items = []

    for i, det in enumerate(detections):
        x1, y1, x2, y2, conf, cls = map(int, det[:6])
        cropped = image[y1:y2, x1:x2]
        filename = f"cropped/item_{i}.jpg"
        cv2.imwrite(filename, cropped)
        items.append(filename)

    return items
