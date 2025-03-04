import random
from typing import List, Tuple
import ollama
from jsonschema import validate, ValidationError
from helpers import save_response_to_file, get_proper_models, clear_terminal
from constants import template, difficulties, styles
from collections import Counter    
import json
from cleanup import cleanup_response, correct_json_using_deepseek_r1, validate_response_content

clear_terminal()

test_json = """
{
  "title": "Sudoku Validator",
  "description": "create a valid JSON string from the given input.",
  "code": "def validate_sudoku(board):\n    # Check rows\n    for row in board:\n        if not isValid(row):\n            return False\n    \n    # Check columns\n    for col in range(9):\n        column = [board[row][col] for row in range(9)]\n        if not isValid(column):\n            return False\n    \n    # Check subgrids\n    for i in range(0, 9, 3):\n        for j in range(0, 9, 3):\n            subgrid = [board[x][y] for x in range(i, i+3) for y in range(j, j+3)]\n            if not isValid(subgrid):\n                return False\n    \n    return True\n    \n    def isValid(arr):\n        arr = [x for x in arr if x != '.']\n        return len(set(arr)) == len(arr)",
  "tests": [
    "test case 1",
    "test case 2",
    "test case 3"
  ]
}
"""
print(test_json)
json.loads(test_json, strict=False)

is_valid, directory = validate_response_content(test_json)
print(is_valid, directory)
#exit()

useful_models = get_proper_models()
print(10*'-')

def ask_codellama(model, content):
    response = ollama.chat(model=model, messages=[{
        'role': 'user',
        'content': content 
    }])

    print("here 1")
    print(response['message']['content'])
    response_content_cleaned = cleanup_response(response['message']['content'])
    print("here 2")
    print(response_content_cleaned)
    print("here 3")

    try:
        is_valid, directory = validate_response_content(response_content_cleaned)
        if is_valid:
           print("here 4 - valid response that needs to be saved ")
           return json.loads(response_content_cleaned, strict=False)
        else:
            save_response_to_file(response_content_cleaned, directory="needs_postprocessing")

            # # this line is so enefficient due to deep seek being so heavy. We will do it in postprocessing instead
            # # corrected_using_deepseek_r1 = correct_json_using_deepseek_r1(response_content_cleaned)
            # try:
            #     is_valid, directory = validate_response_content(corrected_using_deepseek_r1)
            #     if is_valid:
            #         return json.loads(corrected_using_deepseek_r1, strict=False)
            #     else:
            #         # save_response_to_file(corrected_using_deepseek_r1, directory=directory)
            #         return None
            # except (json.JSONDecodeError, ValidationError) as e:
            #     print("\n\n\n")
            #     print(">>>"*40)
            #     print(corrected_using_deepseek_r1)
            #     print("<<<"*40)
            #     print("\n\n\n")
            #     print(f"Invalid JSON or schema: {e}")
            #     return None
            
    except (json.JSONDecodeError, ValidationError) as e:
        print("\n\n\n")
        print(">>>"*40)
        print(response_content_cleaned)
        print("<<<"*40)
        print("\n\n\n")
        print(f"Invalid JSON or schema: {e}")
        return None


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