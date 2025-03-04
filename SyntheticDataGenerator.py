import ollama
import json
from jsonschema import validate, ValidationError
import pynvml
import hashlib
import os
import json
from ollama import ListResponse, list
import random 
from collections import Counter
import re
import ast
import json

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
  "title": "Title for the problem (for example: Palindrome Checker)",
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
        
        response_content_raw = response['message']['content']
        # --- RULES ---
        strings_to_remove = ["Here's your new Python coding question:",
                             "Here is your new Python coding question:",
                             "Here is your new Python coding question:",
                             "Here's your Python coding question:",
                             "Here is the Python coding question:",
                             "Here's the JSON string for your requested Python coding question:",
                             "Here is the medium Python coding question:",
                             "Sure! Here's a new Python coding question for you:",
                             "Here's a new Python coding question for you:",
                             "```json"]
        for string in strings_to_remove:
            response_content_raw = response_content_raw.replace(string, "")
            
        ## TODO -remove 
        response_content_raw = response_content_raw.replace("Here's your new Python coding question:","")
        response_content_raw = response_content_raw.replace("Here is your new Python coding question:", "")
        response_content_raw = response_content_raw.replace("Here is your new Python coding question:", "")
        response_content_raw = response_content_raw.replace("```json","")
        response_content_raw = response_content_raw.strip()
        response_content_raw = response_content_raw.rstrip("```")
        # END OF RULES 
        
        response_content = json.loads(response_content_raw)

        validate(instance=response_content, schema=schema)
        try:
            compile(response_content['code'], '<string>', 'exec')
            # Check if each test is valid Python code
            for test in response_content['tests']:
                try:
                    compile(test, '<string>', 'exec')
                except SyntaxError as e:
                    print(f"Valid JSON response but invalid Python test code: {e}")
                    save_response_to_file(response_content, directory="invalid_tests")
                    return None
            
            print("Valid JSON response with correct schema and valid Python code and tests.")
        except SyntaxError as e:
            save_response_to_file(response_content, directory="invalid_python_code")
            print(f"Valid JSON response but invalid Python code: {e}")
            return None
        
    except (json.JSONDecodeError, ValidationError) as e:
        # save_response_to_file(response['message']['content'], directory="invalid_json")
        print("\n\n\n")
        print(">>>"*40)
        print(response_content_raw)
        print("<<<"*40)
        print("\n\n\n")
        print(f"Invalid JSON or schema: {e}")
        return None
    
    except ValueError as e:
        # save_response_to_file(response['message']['content'], directory="invalid_json")
        print("\n\n\n")
        print(">>>"*40)
        print(response_content_raw)
        print("<<<"*40)
        print("\n\n\n")
        print(f"Invalid JSON or schema: {e}")
        return None
    

    
    return response_content

while True:
    model = random.choice(useful_models)
    fail_counter = 0
    for i in range(100): # Generate 20 questions with each model (this saves on loading the models into the GPU NVRAM 
        if fail_counter > 5:
            break
        content = """
        I want you to generate a **REPLACE WITH DIFFICULTY** python coding question for me in the style of **IN THE STYLE OF** and provide the answer, write the test questions and the function signature. 
        Use the following template as a guide and maintain the formatting strictly. 
        Your returned string should be in the form of json, and have title, description, code and tests keys. 
        The code should be a function that solves the problem. You are expected to put the full functioning code in the code section. 
        The tests should be a list of strings that test the function.
        Use this template as a guide and create other creative python questions. 
        In the title you should also include whether the problem is easy, medium or hard. 
        Please don\'t just create the same palindrome checker that I have provided as an example, you are supposed to create a new question. 
        And you are also supposed to provide the answer to the question in the code section.
        Make sure that your output is in the form of a json string without any extra characters that break the json format. 
        For example avoid using texts like "sure here is your json file" and just give me the json string.
        Also avoid adding the string "```json" to the output string as it will break the json format.
        Absolutely do not reply by "Here's a new Python coding question for you" and instead just give me a json string right away 
        Make sure keys and values of the json string are in double quotes.
        This is the template: 
        """+str(template)
        difficulty = random.choice(difficulties)
        styles = ["LeetCode", "CodeSignal", "HackerRank", "CodeWars", "Project Euler", "Daily Coding Problem", 
                  "Interview Query", "Exercism", "Codecademy", "Codewars", "Internationals Olympiad", "Google Code Jam", 
                  "Facebook Hacker Cup", "Codeforces", "AtCoder", "TopCoder", "Competitive Programming", "ICPC", 
                  "ACM-ICPC", "CodeChef", "HackerEarth", "SPOJ"]
        style = random.choice(styles)
        content = content.replace("**IN THE STYLE OF**", style)
        print(f"Generating {difficulty} question from {model} in the style of {style}...")
        content_with_difficulty = content.replace("**REPLACE WITH DIFFICULTY**", difficulty)
        response = ask_codellama(model, content_with_difficulty)
        

        if response:
            try:
                if all(key in response for key in template.keys()):
                    print(f"Successfully generated {difficulty} question")
                    response['difficulty'] = difficulty
                    response['model'] = model
                    response['style'] = style
                    save_response_to_file(response, directory="data")
                    fail_counter -= 1
                    useful_models.append(model) #increase the probability of using this model again
                else:
                    print(f"Response missing required keys for {difficulty} question")
            except Exception as e:
                print(f"Error processing {difficulty} question: {e}")
        else:
            print(f"Failed to generate {difficulty} question")
            fail_counter += 1
            
        model_counts = Counter(useful_models)
        sorted_model_counts = sorted(model_counts.items(), key=lambda x: x[1], reverse=True)
        print("Model usage counts in descending order:")
        for model, count in sorted_model_counts:
            print(f"{model}: {count}", end=", ")
        print("\n\n\n\n\n\n\n\n\n")