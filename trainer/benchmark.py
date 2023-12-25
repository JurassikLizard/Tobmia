from ultralytics.utils.benchmarks import benchmark
from ultralytics import YOLO
from resources import manager

# try:
#   import torch
#   torch.cuda.set_device(0)
#   # Causes a weird bug with NaN losses if not included
#   torch.backends.cudnn.enabled = False
#   CUDA_AVAILABLE = True
# except:
#   CUDA_AVAILABLE = False


manager.install_remotes()

#benchmark(model=manager.get_resource_path('192model.pt'), data=manager.get_resource_path('fortnite_dataset_small/data.yaml'), imgsz=192, device='cpu')
benchmark(model=manager.get_resource_path('320model.pt'), data=manager.get_resource_path('fortnite_dataset_small/data.yaml'), imgsz=192, device='cpu')