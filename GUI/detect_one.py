import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import time
import torch
from screenshot_dxcam import shot
import os


dirname = os.path.dirname(__file__)

# model = YOLO(dirname + r"\nano224-2.3-9.onnx", task="detect")
model = YOLO(dirname + r"\nano192-1.2-7.onnx", task="detect")


# 0.586 for nano_old


def get_prediction(img):
    results = model.predict(img, imgsz=192, conf=0.3)
    return results


if __name__ == "__main__":
    img = cv2.imread(dirname + r"\test2.webp")
    for x in range(5):
        # img = shot((0, 0, 1920, 1080))
        r = get_prediction(img)
    for box in r[0].boxes:
        x1y1 = [int(x) for x in box.xyxy[0][:2]]
        x2y2 = [int(x) for x in box.xyxy[0][2:]]
        img = cv2.rectangle(img, tuple(x1y1), tuple(x2y2), (244, 113, 115), 2)

    plt.imshow(img, cmap="gray", interpolation="bicubic")
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
