import json 
import ast

from inspect_ai.dataset import Sample
from inspect_ai.dataset import csv_dataset

def load_dataset(path: str, template_path: str):
    with open(template_path, "r") as f:
        template = f.read()

    def record_to_sample(record) -> Sample:
        input_text = template.replace("$PUZZLE$", record["puzzle"])

        return Sample(
            id=record["id"],
            input=input_text,
            target=record["solution_alt"],
            metadata={
                    "size": record["size"], 
                    "puzzle": record["puzzle"],
                    "solution_inst": record["solution_inst"]
                },
        )

    return csv_dataset(path, record_to_sample)


def normalize(s: str) -> str:
    return s.strip().replace(" ", "").replace("_", "").replace("-", "")


def to_lowercase(d: dict) -> dict:
    return {
        k.lower(): to_lowercase(v) if isinstance(v, dict) else v.lower()
        for k, v in d.items()
    }

def str_to_dict(value):
    parsed = ast.literal_eval(value)

    for key, val in parsed.items():
        if isinstance(val, str):
            try:
                parsed[key] = json.loads(val)
            except (json.JSONDecodeError, ValueError):
                pass  # leave it as a string if it's not valid JSON

    return parsed 


    
class Content(str):
    def __new__(cls, path: str, error_msg: str | None = None):
        with open(path, "r") as f:
            content = f.read()
        if error_msg: 
            content = content.replace("$ERROR_MSG$", error_msg)
        return super().__new__(cls, content)


