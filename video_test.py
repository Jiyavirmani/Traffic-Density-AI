from ultralytics import YOLO #you only look once
import cv2 #opencv
import time
import csv

model = YOLO("yolov8n.pt")

qq  # car, motorcycle, bus, truck
#cap = cv2.VideoCapture("data/traffic.mp4")
cap = cv2.VideoCapture("data/traffic.mp4")

# CSV setup
csv_file = open("output/traffic_data.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time", "Vehicles", "Density", "SignalTime", "Alert"])

total_count = 0
counted_ids = set()
previous_positions = {}

#  Vehicle type counts
vehicle_counts = {
    "car": 0,
    "motorcycle": 0,
    "bus": 0,
    "truck": 0
}

# Density variables
start_time = time.time()
interval = 10
interval_count = 0
traffic_density = "Low"
signal_time = 10

# Congestion
high_density_counter = 0

# Peak tracking
peak_count = 0
peak_time = ""

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    line_position = int(frame.shape[0] * 0.7)

    results = model.track(frame, persist=True)

    boxes = results[0].boxes
    annotated_frame = results[0].plot()

    cv2.line(
        annotated_frame,
        (0, line_position),
        (frame.shape[1], line_position),
        (0, 0, 255),
        3
    )

    if boxes.id is not None:
        for box, track_id in zip(boxes, boxes.id):

            cls = int(box.cls[0])
            track_id = int(track_id)

            if cls in vehicle_classes:

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                center_y = (y1 + y2) // 2

                if track_id not in previous_positions:
                    previous_positions[track_id] = center_y

                prev_y = previous_positions[track_id]

                if prev_y < line_position and center_y >= line_position:
                    if track_id not in counted_ids:
                        counted_ids.add(track_id)
                        total_count += 1
                        interval_count += 1

                        # 🚀 NEW: Vehicle type counting
                        if cls == 2:
                            vehicle_counts["car"] += 1
                        elif cls == 3:
                            vehicle_counts["motorcycle"] += 1
                        elif cls == 5:
                            vehicle_counts["bus"] += 1
                        elif cls == 7:
                            vehicle_counts["truck"] += 1

                previous_positions[track_id] = center_y

    current_time = time.time()

    if current_time - start_time >= interval:

        if interval_count <= 5:
            traffic_density = "Low"
        elif interval_count <= 15:
            traffic_density = "Medium"
        else:
            traffic_density = "High"

        # Signal
        if traffic_density == "Low":
            signal_time = 10
        elif traffic_density == "Medium":
            signal_time = 30
        else:
            signal_time = 60

        # Congestion
        if traffic_density == "High":
            high_density_counter += 1
        else:
            high_density_counter = 0

        # Peak
        if interval_count > peak_count:
            peak_count = interval_count
            peak_time = time.strftime("%H:%M:%S")

        # CSV
        timestamp = time.strftime("%H:%M:%S")
        alert_status = "YES" if high_density_counter >= 2 else "NO"

        csv_writer.writerow([
            timestamp,
            interval_count,
            traffic_density,
            signal_time,
            alert_status
        ])

        interval_count = 0
        start_time = current_time

    # DISPLAY

    cv2.putText(
        annotated_frame,
        f"Total Vehicles: {total_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    if traffic_density == "Low":
        density_color = (0, 255, 0)
    elif traffic_density == "Medium":
        density_color = (0, 255, 255)
    else:
        density_color = (0, 0, 255)

    cv2.putText(
        annotated_frame,
        f"Density: {traffic_density}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        density_color,
        3
    )

    cv2.putText(
        annotated_frame,
        f"Signal: {signal_time}s",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    if high_density_counter >= 2:
        cv2.putText(
            annotated_frame,
            "TRAFFIC JAM DETECTED",
            (20, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.putText(
        annotated_frame,
        f"Peak: {peak_count} at {peak_time}",
        (20, 210),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    # 🚀 NEW DISPLAY
    cv2.putText(
        annotated_frame,
        f"Cars: {vehicle_counts['car']} Bikes: {vehicle_counts['motorcycle']}",
        (20, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        annotated_frame,
        f"Buses: {vehicle_counts['bus']} Trucks: {vehicle_counts['truck']}",
        (20, 280),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow("AI Traffic Monitoring System", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

csv_file.close()
cap.release()
cv2.destroyAllWindows()