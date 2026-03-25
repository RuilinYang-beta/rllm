from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import exact
from inspect_ai.solver import generate
from inspect_ai.dataset import FieldSpec, csv_dataset

from scorers import max_dict_match
from subset_data import SAVE_PATH, DEV_SAVE_PATH

TEMPLATE_ONE_SHOT_PATH = "./prompts/template_one_shot.txt"

def load_dataset(path: str, template_path: str):
    with open(template_path, "r") as f:
        template = f.read()

    def record_to_sample(record) -> Sample:
        # input_text = template.replace("$PUZZLE$", record["puzzle"]) \
        #                     .replace("$SOLUTION_INST$", record["solution_inst"])
        
        # no JSON in instruction, just the puzzle:
        input_text = template.replace("$PUZZLE$", record["puzzle"])

        return Sample(
            id=record["id"],
            input=input_text,
            target=record["solution_alt"],
            metadata={"size": record["size"]},
        )

    return csv_dataset(path, record_to_sample)

@task
def naive_cot():
    return Task(
        # dataset=load_dataset(SAVE_PATH, TEMPLATE_ONE_SHOT_PATH)
        dataset=load_dataset(SAVE_PATH, TEMPLATE_ONE_SHOT_PATH).filter(
                lambda sample : sample.metadata["size"] == "6*6"
            ),
        solver=[generate()],
        scorer=max_dict_match(),
    )