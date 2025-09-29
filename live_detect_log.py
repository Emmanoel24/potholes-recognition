from ultralytics import YOLO
import cv2
import pyttsx3
import pandas as pd
from datetime import datetime

# 1️⃣ Load model
model = YOLO("models/road_model.pt")

# 2️⃣ Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# 3️⃣ Webcam
cap = cv2.VideoCapture(0)

# 4️⃣ CSV setup
log_file = "detections_log.csv"
df = pd.DataFrame(columns=["timestamp", "class", "confidence", "frame"])
df.to_csv(log_file, index=False)  # create file with headers

frame_count = 0
spoken_recently = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1

    results = model(frame)
    annotated = results[0].plot()

    # detection flag
    pothole_detected = False

    for box in results[0].boxes:
        cls_id = int(box.cls)
        conf = float(box.conf)
        cls_name = model.names[cls_id]

        # ✅ save detection
        row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "class": cls_name,
            "confidence": round(conf, 2),
            "frame": frame_count
        }
        df = pd.DataFrame([row])
        df.to_csv(log_file, mode="a", header=False, index=False)

        if cls_name.lower() == "pothole":
            pothole_detected = True

    # Voice alert (only once per frame)
    if pothole_detected and not spoken_recently:
        engine.say("⚠ Danger! Pothole ahead.")
        engine.runAndWait()
        spoken_recently = True
    elif not pothole_detected:
        spoken_recently = False

    cv2.imshow("🚗 RoadSense AI - Logging Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("✅ Detection logging completed. All results saved to detections_log.csv")