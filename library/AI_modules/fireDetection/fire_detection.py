# Author: Bang Do Van
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Load model
model = YOLO("library/AI_modules/fireDetection/best.pt")


# Predict and get the results
model.predict(source=0, imgsz=640, conf=0.5, show=False)