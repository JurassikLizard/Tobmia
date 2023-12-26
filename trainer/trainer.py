import argparse
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

def train_model(args):
  manager.install_remotes()
  settings.update({'datasets_dir':manager.get_resource_path("")})
  
  with open(os.path.join(os.path.dirname(__file__), 'trainer.log'), 'w') as f:
    f.write('model: ' + args.model + '\n')
    f.write('dataset: ' + args.dataset + '\n')
  
  model = YOLO(manager.get_resource_path(args.model))
  model.info()
  results = model.train(data=os.path.abspath('resources/local/' + args.dataset + '/data.yaml'), 
                        epochs=1, 
                        imgsz=192, 
                        project=os.path.join(os.path.dirname(__file__), 'runs'),
                        name='run')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Train YOLO model on Fortnite dataset')
  parser.add_argument('-m', '--model', help='Model name in remotes (e.g. small_v8.pt)', required=True)
  parser.add_argument('-d', '--dataset', help='Dataset name in remotes without .zip (e.g. fortnite_dataset_192)', required=True)
  args = parser.parse_args()
  
  train_model(args)