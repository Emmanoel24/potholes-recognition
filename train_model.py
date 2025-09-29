from ultralytics import YOLO

# Load a small pre-trained YOLO model so I don't have to train from scratch
model = YOLO("yolov8n.pt")

# Train the model using my custom road data (potholes + vehicles)
# I set epochs to 50 so the model sees the data many times and learns properly
model.train(
    data="C:/Users/OWNER/Desktop/road_vision/data/data.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
)

# Export the final trained model so I can load it later in the web app
model.export(format="onnx")