import ollama
import json
from jsonschema import validate, ValidationError
import pynvml
import hashlib
import os
import json
from ollama import ListResponse, list
import random 


def save_response_to_file(response_content):
    # Generate a hash of the title
    title_hash = hashlib.md5(response_content['title'].encode()).hexdigest()
    
    # Define the directory and file path
    directory = 'data'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{title_hash}.json")
    
    # Save the response content to the file
    with open(file_path, 'w') as file:
        json.dump(response_content, file, indent=4)
    
    print(f"Response saved to {file_path}")

response: ListResponse = list()

def get_nvram_size():
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    nvram_size = info.total
    pynvml.nvmlShutdown()
    return nvram_size

nvram_size = get_nvram_size()
print(f"Total NVRAM size: {nvram_size / (1024 ** 3):.2f} GB")
useful_models = []

for model in  response.models:
    size = model.size.real
    if size < nvram_size:
        print(model["model"] + "----" + str(f'{size/ (1024 ** 3):.2f} GB'))
        useful_models.append(model["model"])

difficulties = ["easy", "medium", "hard", "super hard", "insanely difficult"]


template = {
  "title": "Title for the problem (for example: Easy - Palindrome Checker)",
  "description": "A description of the problem in string form, the description may contain function signature, input format, output format, constraints and hints. Example: A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization). Write a function `is_palindrome` that checks if a given string is a palindrome.\n\n#### Function Signature\n```python\ndef is_palindrome(s: str) -> bool:\n```\n\n#### Input\n- `s` (str): A string that may contain letters, numbers, spaces, and punctuation.\n\n#### Output\n- Returns `True` if the input string is a palindrome, `False` otherwise.\n",
   "code": "import string\n\ndef is_palindrome(s: str) -> bool:\n    # Convert to lowercase\n    s = s.lower()\n    # Remove non-alphanumeric characters\n    s = ''.join(char for char in s if char in string.ascii_letters + string.digits)\n    # Check if the string reads the same forwards and backwards\n    return s == s[::-1]\n",
  "tests": [
    "assert is_palindrome(\"A man, a plan, a canal, Panama\") == True",
    "assert is_palindrome(\"racecar\") == True",
    "assert is_palindrome(\"hello\") == False",
    "assert is_palindrome(\"No 'x' in Nixon\") == True"
  ]
}



print(10*'-')
def ask_codellama(model, content):
    response = ollama.chat(model=model, messages=[{
        'role': 'user',
        'content': content 
    }])

    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "code": {"type": "string"},
            "tests": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["title", "description", "code", "tests"]
    }
    print(response['message']['content'])
    try:
        response_content = json.loads(response['message']['content'])
        
        

        validate(instance=response_content, schema=schema)
        try:
            compile(response_content['code'], '<string>', 'exec')
            # Check if each test is valid Python code
            for test in response_content['tests']:
                try:
                    compile(test, '<string>', 'exec')
                except SyntaxError as e:
                    print(f"Valid JSON response but invalid Python test code: {e}")
                    return None
            
            print("Valid JSON response with correct schema and valid Python code and tests.")
        except SyntaxError as e:
            print(f"Valid JSON response but invalid Python code: {e}")
            return None
        
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Invalid JSON or schema: {e}")
        return None
    

    
    return response_content

while True:
    model = random.choice(useful_models)
    for i in range(20): # Generate 20 questions with each model (this saves on loading the models into the GPU NVRAM 
        content = """
        I want you to generate a **REPLACE WITH DIFFICULTY** python coding question for me and provide the answer, write the test questions and the function signature. 
        Use the following template as a guide and maintain the formatting strictly. 
        Your returned string should be in the form of json, and have title, description, code and tests keys. 
        The code should be a function that solves the problem. You are expected to put the full functioning code in the code section. 
        The tests should be a list of strings that test the function.
        Use this template as a guide and create other creative python questions. 
        In the title you should also include whether the problem is easy, medium or hard. 
        Please don\'t just create the same palindrome checker that I have provided as an example, you are supposed to create a new question. 
        And you are also supposed to provide the answer to the question in the code section.
        This is the template: 
        """+str(template)
        difficulty = random.choice(difficulties)
        print(f"Generating {difficulty} question from {model}...")
        content_with_difficulty = content.replace("**REPLACE WITH DIFFICULTY**", difficulty)
        response = ask_codellama(model, content_with_difficulty)
        

        if response:
            try:
                if all(key in response for key in template.keys()):
                    print(f"Successfully generated {difficulty} question")
                    save_response_to_file(response)
                else:
                    print(f"Response missing required keys for {difficulty} question")
            except Exception as e:
                print(f"Error processing {difficulty} question: {e}")
        else:
            print(f"Failed to generate {difficulty} question")