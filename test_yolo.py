from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # lightweight model
results = model("https://ultralytics.com/images/bus.jpg", show=True)

print("Model ran successfully!")