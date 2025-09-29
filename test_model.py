import os
from ultralytics import YOLO
import cv2

# 1️⃣ Load your trained model
model = YOLO("models/road_model.pt")

# 2️⃣ Choose an image to test
image_path = "data/val/images/potholes538.png"  # 👈🏽 replace with any real image filename

# 3️⃣ Run the prediction (YOLO will save the result in a new folder)
results = model.predict(source=image_path, save=True, show=False)

# 4️⃣ Automatically detect the latest 'predict' folder
detect_dir = "C:/Users/OWNER/runs/detect"
latest_run = sorted([d for d in os.listdir(detect_dir) if d.startswith("predict")], key=lambda x: os.path.getmtime(os.path.join(detect_dir, x)))[-1]
latest_path = os.path.join(detect_dir, latest_run)

# 5️⃣ Find the first image inside that folder
for file in os.listdir(latest_path):
    if file.lower().endswith((".jpg", ".png")):
        output_path = os.path.join(latest_path, file)
        break

# 6️⃣ Display the result
img = cv2.imread(output_path)
cv2.imshow("✅ Detection Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"✅ Detection complete. Result shown from: {output_path}")