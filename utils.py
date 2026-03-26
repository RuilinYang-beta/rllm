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


    
class Feedback(str):
    def __new__(cls, path: str, error_msg: str | None = None):
        with open(path, "r") as f:
            content = f.read()
        if error_msg: 
            content = content.replace("$ERROR_MSG$", error_msg)
        return super().__new__(cls, content)


    