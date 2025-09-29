from ultralytics import YOLO

model = YOLO("models/road_model.pt")
print(model.names)