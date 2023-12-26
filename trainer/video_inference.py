from ultralytics import YOLO
from resources import manager
import os
import cv2 as cv
import numpy as np

def split():
  pass

def show_images():
  cap = cv.VideoCapture('video.mp4')
  model = YOLO(manager.get_resource_path('models/nano192-1.2-7.onnx'), task='detect')
  
  while cap.isOpened():
    ret, frame = cap.read()
    
    # if frame is read correctly ret is True
    if not ret:
      print("Can't receive frame (stream end?). Exiting ...")
      break
    
    frame = cv.resize(frame, (576, 576))
    
    results = model.predict(frame, imgsz=192, conf=0.509, verbose=False, task='detect', device='cpu')
    for part_box in results[0].boxes:
      box = part_box.xyxy[0]
      x1y1 = (int(box[0]), int(box[1]))
      x2y2 = (int(box[2]), int(box[3]))
      frame = cv.rectangle(frame, x1y1, x2y2, (244, 113, 115), 2)
      
      #frame = cv.resize(frame, (576, 576))
    
    # for i in range(0, 576, 192):
    #     for j in range(0, 576, 192):
    #         part = frame[i:i+192, j:j+192]
    #         results = model.predict(part, imgsz=192, conf=0.43, verbose=False, task='detect', device='cpu')
    #         for part_box in results[0].boxes:
    #           box = part_box.xyxy[0]
    #           x1y1 = (int(box[0]+i), int(box[1]+j))
    #           x2y2 = (int(box[2]+i), int(box[3]+j))
    #           frame = cv.rectangle(frame, x1y1, x2y2, (244, 113, 115), 2)
    
    cv.imshow('frame', frame)
    
    if cv.waitKey(1) == ord('q'):
        break
  cap.release()
  cv.destroyAllWindows()

if __name__ == '__main__':
  manager.install_remotes()
  show_images()