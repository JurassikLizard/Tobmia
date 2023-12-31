import json
from tqdm import tqdm
import requests
import zipfile
import os
from os import path

def get_resource_names() -> list:
  return os.listdir(path.join(path.dirname(__file__), 'local/'))

def get_resource_path(name) -> str:
  return path.join(path.dirname(__file__), "local/"+name)

def check_extension(file):
  name = file.split('.')[0]
  ext = file.split('.')[1]
  
  if ext == 'pt':
    pass
  elif ext == 'zip':
    with zipfile.ZipFile(get_resource_path(file), 'r') as zip_ref:
     zip_ref.extractall(get_resource_path(name + '/'))
  else:
    raise Exception('Unknown file extension in remotes!')

def install_remotes() -> bool:
  current_dir = path.dirname(__file__)
  remotes_file = path.join(current_dir, 'remotes.json')
  existing_resources = get_resource_names()
  
  with open(remotes_file, 'r') as data:
    remotes = json.load(data)
    for remote in remotes['download']:
      # TODO: Use rich console
      print('Downloading remote: ' + remote['url'])
      
      # Check if resource already downloaded
      if remote['local'] in existing_resources:
        # TODO: Use rich console
        print('Already downloaded...')
        continue
      
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