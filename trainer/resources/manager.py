import json
from tqdm import tqdm
import requests
import zipfile
import os
from os import path

def get_resource_path(name) -> str:
  return path.join(path.dirname(__file__), "local/"+name).replace("\\","/")

def check_extension(file):
  name = file.split('.')[0]
  ext = file.split('.')[1]
  
  if ext == 'pt' or ext =='onnx' or ext=='torchscript':
    pass
  elif ext == 'zip':
    with zipfile.ZipFile(get_resource_path(file), 'r') as zip_ref:
     zip_ref.extractall(get_resource_path(name + '/'))
  else:
    raise Exception('Unknown file extension in remotes!')

def manage_remote_item_groups(items):
  out = []
  for i in items:
    if 'group' in i:
      for j in i['download']:
        j['local'] = i['group'] + '/' + j['local']
        out.append(j)
    else:
      out.append(i)
  return out

def install_remotes() -> bool:
  current_dir = path.dirname(__file__)
  remotes_file = path.join(current_dir, 'remotes.json')
  
  with open(remotes_file, 'r') as data:
    remotes = json.load(data)
    remote_items = remotes['download']
    
    remote_items = manage_remote_item_groups(remote_items)
    
    for remote in remote_items:
      # TODO: Use rich console
      print('Downloading remote: ' + remote['url'])
      
      # Check if resource already downloaded
      if path.exists(get_resource_path(remote['local'])):
        # TODO: Use rich console
        print('Already downloaded...')
      else:
        # Get info from remotes.json
        url = remote['url']
        response = requests.get(url, stream=True)
        
        # Setup data for progress bar
        file_size = int(response.headers.get('content-length', 0))
        block_size = 1024 #1 Kilobyte
        
        # Init progress bar and stream download to file
        progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True)
        with open(path.join(current_dir, "local/"+remote['local']), 'wb') as file:
          for data in response.iter_content(block_size):
              progress_bar.update(len(data))
              file.write(data)
        progress_bar.close()
        
        # TODO: Use rich console
        if file_size != 0 and progress_bar.n != file_size:
          raise Exception("ERROR, something went wrong downloading remote!")
      
      check_extension(remote['local'])
      
      # Remote done
      print('Done!')