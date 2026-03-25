import json 
import ast

def str_to_dict(value):
    parsed = ast.literal_eval(value)

    for key, val in parsed.items():
        if isinstance(val, str):
            try:
                parsed[key] = json.loads(val)
            except (json.JSONDecodeError, ValueError):
                pass  # leave it as a string if it's not valid JSON

    return parsed 

