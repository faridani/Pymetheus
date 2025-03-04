from ollama import ListResponse, list
import pynvml
import hashlib
import json 
import os 
from typing import List

def save_response_to_file(response_content, directory):
    # Generate a hash of the title
    title_hash = hashlib.md5(str(response_content).encode()).hexdigest()
    
    # Define the directory and file path
    directory = directory
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{title_hash}.json")
    
    # Save the response content to the file
    with open(file_path, 'w') as file:
        json.dump(response_content, file, indent=4)
    
    print(f"Response saved to {file_path}")

def get_nvram_size():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    nvram_size = info.total
    pynvml.nvmlShutdown()
    return nvram_size



def get_proper_models()-> List[str]:
    nvram_size = get_nvram_size()

    print(f"Total NVRAM size: {nvram_size / (1024 ** 3):.2f} GB")

    response: ListResponse = list()

    useful_models = []

    for model in  response.models:
        size = model.size.real
        if size < nvram_size:
            print(model["model"] + "----" + str(f'{size/ (1024 ** 3):.2f} GB'))
            useful_models.append(model["model"])
    return useful_models

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
