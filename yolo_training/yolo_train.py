from ultralytics import YOLO

# Wczytanie modelu YOLOv8
model = YOLO('yolov8n.pt')  # Wybierz model YOLOv8 (nano, small, medium, etc.)

# Trenowanie modelu
model.train(data=r'/home/szewczyk/Desktop/dataset.yaml', epochs=2, imgsz=320)