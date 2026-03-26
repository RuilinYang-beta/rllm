from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.solver import generate, system_message
from inspect_ai.dataset import FieldSpec, csv_dataset

from scorers import max_cell_match
from subset_data import SAVE_PATH
from utils import Content

TEMPLATE_COT_PATH = "./prompts/template_cot.txt"
# reduce the chance of triggering content violation policy 
SYSTEM_MESSAGE_PATH = "./prompts/system_cot.txt"


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

@task
def naive_cot():
    return Task(
        dataset=load_dataset(SAVE_PATH, TEMPLATE_COT_PATH),
        
        # dataset=load_dataset(SAVE_PATH, TEMPLATE_ONE_SHOT_PATH).filter(
        #         lambda sample : sample.metadata["size"] == "6*6"
        #     )[:1], # just one big sample for testing
        
        solver=[system_message(Content(SYSTEM_MESSAGE_PATH)), generate()],
        scorer=max_cell_match(),
    )