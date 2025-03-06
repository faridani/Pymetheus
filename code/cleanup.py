import json
from jsonschema import validate, ValidationError
import ollama
from typing import Tuple
from repair_json import repair_json_string
def validate_response_content(s: str)-> Tuple[bool, str]:
                # bool: whether the response is valid
                # str: is the directory that the result should be storied in 
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
                try:
                    print("trying to load the json ")
                    r = json.loads(s, strict=False)
                    print("loaded the json and it is fine, next trying the schema validation")
                    try:
                        validate(instance=r, schema=schema)
                        print("schema validation passed")
                        try:
                            compile(r['code'], '<string>', 'exec')
                            for test in r['tests']:
                                try:
                                    compile(test, '<string>', 'exec')
                                except SyntaxError as e:    
                                    print(f"Valid JSON response and python but invalid tests code: {e}")
                                    return (False, "invalid_tests")
                                   
                        except SyntaxError as e:
                            print(f"Valid JSON response and but invalid python code: {e}")
                            return (False, "invalid_python_code")
                    except ValidationError as e:
                        print(f"Valid JSON response but invalid schema: {e.message}")
                        return (False, "invalid_json")
                except json.JSONDecodeError as e:
                    return (False, "invalid_json")
                
                return (True, "good_quality")
     
def cleanup_response(response_content_raw):
            
            # --- RULES ---
            strings_to_remove = ["Here's your new Python coding question:",
                                 "Here is your Python coding question:",
                                 "Here's your requested Python coding question:",
                                "Here is your new Python coding question:",
                                "Here is your new Python coding question:",
                                "Here's your Python coding question:",
                                "Here is the Python coding question:",
                                "Here's the JSON string for your requested Python coding question:",
                                "Here is the medium Python coding question:",
                                "Sure! Here's a new Python coding question for you:",
                                "Here's a new Python coding question for you:",
                                "Here is a new Python coding question for you:",
                                "Here's your JSON string:",
                                "Here's a JSON string that satisfies the requirements mentioned in the template:",
                                "Here's your new problem as a JSON string:",
                                "Here's a new problem as a JSON string:",
                                "```json"]
            for string in strings_to_remove:
                response_content_raw = response_content_raw.replace(string, "")
            response_content_raw = response_content_raw.strip()
            response_content_raw = response_content_raw.strip('\n')
            response_content_raw = response_content_raw.rstrip("```")
            while "<think>" in response_content_raw and "</think>" in response_content_raw:
                start = response_content_raw.find("<think>")
                end = response_content_raw.find("</think>") + len("</think>")
                response_content_raw = response_content_raw[:start] + response_content_raw[end:]
            try: 
                response_content_raw = repair_json_string(response_content_raw)
            except ValueError as e:
                pass
            return response_content_raw
    

def correct_json_using_deepseek_r1(s: str) -> str:
    content = "create a valid json string out of this string. Try to maintain the title, description, code, test keys and make it imidiately json parsable   " + s
    response = ollama.chat(model="deepseek-r1:32b", messages=[{
        'role': 'user',
        'content': content 
    }])
    mkdown = response['message']['content']
    if "```json" in mkdown:
        json_str = mkdown.split('```json')[1].split('```')[0].strip()
    else:
        json_str = mkdown
        
    return json_str

 