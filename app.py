from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
import os
import pyttsx3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import threading

app = Flask(__name__)
model = YOLO("models/best.pt")

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No file selected", 400

    # ✅ Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # ✅ Run YOLO detection
    results = model.predict(source=filepath, save=True, conf=0.1)
    result_dir = results[0].save_dir
    for r in results:
        for box in r.boxes:
            print("Class:", model.names[int(box.cls)], " | Confidence:", float(box.conf))
    # ✅ Find saved result image
    result_img_path = None
    for f in os.listdir(result_dir):
        if f.lower().endswith((".jpg", ".png")):
            result_img_path = os.path.join(result_dir, f)
            break

    if result_img_path is None:
        return "❌ No result image found", 500

    new_path = os.path.join(RESULT_FOLDER, "result.jpg")
    os.replace(result_img_path, new_path)

    # ✅ Count detections
    detections = results[0].boxes
    num_detections = len(detections)
    print("Detections found:", num_detections)

    # ✅ Check if pothole detected
    pothole_found = False
    for box in detections:
        cls_id = int(box.cls)
        cls_name = model.names[cls_id].lower()
        print("Detected class:", cls_name)
        if "pothole" in cls_name:
            pothole_found = True
            break

    # ✅ Voice alert threading
    def speak_alert(message):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say(message)
        engine.runAndWait()

    # 🔊 Always speak test message
    threading.Thread(target=speak_alert, args=("🚀 Voice test from inside Flask! It works!",)).start()

    # 🔊 Only speak if pothole is found
    if pothole_found:
        threading.Thread(target=speak_alert, args=("⚠ Warning! Pothole detected in the uploaded image.",)).start()

    # ✅ Return result page
    return render_template("result.html", result_image=new_path, num_detections=num_detections)

@app.route("/analytics")
def analytics():
    df = pd.read_csv("detections_log.csv")

    # Plot class distribution
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="class", palette="coolwarm")
    plt.title("Detection Class Distribution")
    plt.savefig("static/results/class_distribution.png")
    plt.close()

    # Plot confidence distribution
    plt.figure(figsize=(7, 5))
    sns.histplot(df["confidence"], bins=20, kde=True, color="green")
    plt.title("Confidence Score Distribution")
    plt.savefig("static/results/confidence_distribution.png")
    plt.close()

    return render_template("analytics.html")

if __name__ == "__main__":
    app.run(debug=True)