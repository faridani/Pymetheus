from repair_json import repair_json_string
import os
import json
from cleanup import validate_response_content, correct_json_using_LLM
import random
import os 
from helpers import clear_terminal, save_response_to_file
clear_terminal()

import demjson3
import json
from json_repair import repair_json

def fix_json(malformed_str: str) -> str:
    """
    Repairs a malformed JSON string into a correctly formatted JSON string.

    This function attempts to fix common JSON errors such as missing quotes, single quotes,
    trailing commas, unquoted keys, comments, mismatched brackets, and more. It first uses
    demjson3 with lenient parsing settings. If that fails, it falls back to json_repair
    and verifies the result with json.loads. Returns None if the string cannot be repaired.

    Args:
        malformed_str (str): The malformed JSON string to repair.

    Returns:
        str: A correctly formatted JSON string if repair succeeds, otherwise None.

    Examples:
        >>> fix_json('{"key": "value",}')  # Trailing comma
        '{"key": "value"}'
        >>> fix_json("{key: 'value'}")  # Unquoted key, single quotes
        '{"key": "value"}'
        >>> fix_json('{"key": "value')  # Missing closing brace
        '{"key": "value"}'
    """
    # Ensure input is a string
    if not isinstance(malformed_str, str):
        raise TypeError("Input must be a string")

    # Step 1: Try parsing with demjson3 using lenient settings
    try:
        parsed = demjson3.decode(malformed_str,
                                 allow_unquoted_keys=True,
                                 allow_single_quotes=True,
                                 allow_trailing_commas=True,
                                 allow_comments=True)
        # Serialize the parsed object to a valid JSON string
        return json.dumps(parsed)
    except ValueError:
        return malformed_str
    except demjson3.JSONDecodeError:
        # Step 2: If demjson3 fails, attempt repair with json_repair
        repaired_str = repair_json(malformed_str)
        try:
            # Verify the repaired string is valid JSON
            json.loads(repaired_str)
            return repaired_str
        except json.JSONDecodeError:
            # Return None if repair fails
            return None

directory = '../data/needs_postprocessing'
success, fail = 0,0 
files = list(os.listdir(directory))
random.shuffle(files)

for filename in files:
    
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            file_content = file.read()
            # file_content = fix_json(file_content)
            repaired_content = repair_json_string(str(json.loads(file_content)))
            repaired_content = correct_json_using_LLM(repaired_content)
            repaired_content += "}"
           
            print("----"*40)
            print(repaired_content)
            print("----"*40)
            try:
                response = json.loads(repaired_content, strict=False)
            except json.decoder.JSONDecodeError as e:
                fail = fail + 1
                print(f"Success: {success}, Fail: {fail}")      
                continue  
            response = json.loads(repaired_content, strict=False)   
            is_valid, _ = validate_response_content(json.dumps(response["response"]))
            print("----"*40)
            if is_valid:
                success = success + 1
                outputjson = response["response"]
                outputjson['model'] = response["model"]+"-repaired by Llama 3"
                
                save_response_to_file(outputjson, directory="repaired_needs_postprocessing_files")
            else:
                fail = fail + 1
                print("\n\n\n\n\n-----------DEBUGGING FILE----------------")
                print(repaired_content)
                print("-----------END OF DEBUGGING FILE----------------\n\n\n\n")
                
                fail = fail + 1
            print(f"Success: {success}, Fail: {fail}")

print(f"Success: {success}, Fail: {fail}")
