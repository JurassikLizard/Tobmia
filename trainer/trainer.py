from resources import manager
from ultralytics import YOLO
from ultralytics import settings
import os

try:
  import torch
  torch.cuda.set_device(0)
  # Causes a weird bug with NaN losses if not included
  torch.backends.cudnn.enabled = False
  CUDA_AVAILABLE = True
except:
  CUDA_AVAILABLE = False

def train_model():
  manager.install_remotes()
  settings.update({'datasets_dir':manager.get_resource_path("")})
  
  model = YOLO(manager.get_resource_path('nano_v8.pt'))
  model.info()
  results = model.train(data=os.path.abspath('resources/local/fortnite_dataset_small/data.yaml'), 
                        epochs=100, 
                        imgsz=192, 
                        project=os.path.join(os.path.dirname(__file__), 'runs'),
                        name='run')

if __name__ == '__main__':
  train_model()