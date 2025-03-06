from typing import List
import os
import json
import hashlib
import pynvml
from ollama import ListResponse, list


def get_parent_directory_of_script():
    """
    Gets the absolute path of the parent directory of the currently running script.

    Returns:
        str: The absolute path of the parent directory.
    """
    # Get the absolute path of the currently running script
    script_path = os.path.abspath(__file__)

    # Get the directory of the script
    script_directory = os.path.dirname(script_path)

    # Get the parent directory of the script's directory
    parent_directory = os.path.dirname(script_directory)

    return parent_directory

def save_response_to_file(response_content, directory):
    # Generate a hash of the title
    title_hash = hashlib.md5(str(response_content).encode()).hexdigest()
    
    # get a string for the directory and create that directory at the parent location under the subfolder 'data'
    
    # get a string for the directory and create that directory at the parent location under the subfolder 'data'
    parent_directory = get_parent_directory_of_script()
    # Define the directory and file path
    directory = os.path.join(parent_directory, "data", directory)  
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{title_hash}.json")
    
    # Save the response content to the file
    with open(file_path, 'w') as file:
        json.dump(response_content, file, indent=4)
    
    print(f"Response saved to {file_path}")

def get_nvram_size():
    """
    Retrieves the total size of the NVRAM (Non-Volatile Random-Access Memory) of the first GPU device.
    Returns:
        int: The total size of the NVRAM in bytes.
    """
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    nvram_size = info.total
    pynvml.nvmlShutdown()
    return nvram_size



def get_proper_models()-> List[str]:
    nvram_size = get_nvram_size()
    print(f"Total NVRAM size: {nvram_size / (1024 ** 3):.2f} GB\n\n")
    print("Retrieving available models from Ollama...")

    response: ListResponse = list()

    useful_models = []

    for model in  response.models:
        size = model.size.real
        if size < nvram_size:
            print(model["model"] + "----" + str(f'{size/ (1024 ** 3):.2f} GB'))
            useful_models.append(model["model"])
    return useful_models

def clear_terminal():
    """
    Clears the terminal screen.
    Uses 'cls' command for Windows (NT) systems and 'clear' command for Unix-based systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
