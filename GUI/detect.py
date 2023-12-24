import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import time
import torch
from screenshot import shot
import os

dirname = os.path.dirname(__file__)


def modify_img(img):
    square_size = max(img.shape[0], img.shape[1])  # get the larger dimension
    square_image = cv2.resize(img, (square_size, square_size))
    return cv2.resize(square_image, (960, 960))


def get_parts(img):
    h, w = img.shape[:2]
    h_split = h // 3
    w_split = w // 3
    parts = []
    for i in range(3):
        for j in range(3):
            part = img[i * h_split : (i + 1) * h_split, j * w_split : (j + 1) * w_split]
            parts.append(part)
    return parts


def calculate_boxes(parts, model):
    imgs = []
    idx = 0
    for part in parts:
        if idx != 0 and idx != 2 and idx != 6 and idx != 7 and idx != 8:
            start = time.time()
            results = model(part)
            print("{0} ms".format((time.time() - start) * 1000))
            for box in results[0].boxes:
                x1y1 = [int(x) for x in box.xyxy[0][:2]]
                x2y2 = [int(x) for x in box.xyxy[0][2:]]
                part = cv2.rectangle(part, tuple(x1y1), tuple(x2y2), (244, 113, 115), 2)
                # print(box.xyxy)
        imgs.append(part)
        idx += 1
    return imgs


img = cv2.imread(dirname + r"\test2.webp")
model = YOLO(dirname + r"\best.pt")
model.conf = 0.4

img = modify_img(img)
parts = get_parts(img)
parts = calculate_boxes(parts, model)
fig, axs = plt.subplots(3, 3, figsize=(10, 10))
for i, ax in enumerate(axs.flat):
    ax.imshow(parts[i])
plt.show()
