from ultralytics import YOLO
import os
from sklearn.metrics import confusion_matrix, classification_report

model = YOLO("yolov8n.pt")

image_folder = "coco128/images/train2017"
label_folder = "coco128/labels/train2017"

y_true = []
y_pred = []

for img_name in os.listdir(image_folder)[:50]:

    img_path = os.path.join(image_folder, img_name)
    label_path = os.path.join(label_folder, img_name.replace(".jpg", ".txt"))

    # 👉 Get ONE ground truth (first object only)
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            labels = f.readlines()
            if len(labels) == 0:
                continue
            true_cls = int(labels[0].split()[0])
            y_true.append(true_cls)
    else:
        continue

    # 👉 Get ONE prediction (highest confidence)
    results = model(img_path)
    boxes = results[0].boxes

    if boxes is not None and len(boxes) > 0:
        pred_cls = int(boxes.cls[0])
        y_pred.append(pred_cls)
    else:
        y_pred.append(-1)  # no detection

# Ensure same length
min_len = min(len(y_true), len(y_pred))
y_true = y_true[:min_len]
y_pred = y_pred[:min_len]

# 🔥 PRINT RESULTS
print("Total samples:", len(y_true))

cm = confusion_matrix(y_true, y_pred)
print("\nConfusion Matrix:\n", cm)

print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, zero_division=0))