from ultralytics import YOLO
import cv2
import pyttsx3

# 1️⃣ Load the trained model
model = YOLO("models/road_model.pt")

# 2️⃣ Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)   # speed of voice
engine.setProperty('volume', 1.0) # 0.0 - 1.0

# 3️⃣ Start webcam
cap = cv2.VideoCapture(0)

spoken_recently = False  # To avoid repeating voice every frame

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 4️⃣ Make predictions
    results = model(frame)
    annotated_frame = results[0].plot()

    pothole_detected = False

    for cls_id in results[0].boxes.cls:
        if int(cls_id) == 0:  # Assuming 'pothole' is class 0
            pothole_detected = True

    # 5️⃣ Speak once if pothole is detected
    if pothole_detected and not spoken_recently:
        engine.say("⚠ Danger! Pothole ahead.")
        engine.runAndWait()
        spoken_recently = True
    elif not pothole_detected:
        spoken_recently = False

    # 6️⃣ Show live feed
    cv2.imshow("🚗 RoadSense AI - Live Pothole Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()