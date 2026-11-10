from ultralytics import YOLO
import os

model = YOLO("yolov8n.pt")

# Path to dataset images
image_folder = "coco128/images/train2017"

images = os.listdir(image_folder)

for img in images[:20]:  # only first 20 images (fast)
    img_path = os.path.join(image_folder, img)

    results = model(img_path)

    print(f"Processed: {img}")