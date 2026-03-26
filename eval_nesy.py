from inspect_ai import task, Task
from inspect_ai.solver import chain
from inspect_ai import Task, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import exact
from inspect_ai.solver import generate, system_message
from inspect_ai.dataset import FieldSpec, csv_dataset

from scorers import max_cell_match, dummy_scorer
from subset_data import SAVE_PATH, DEV_SAVE_PATH
from solvers import symbolic_solver, format_solver



TEMPLATE_NESY_PATH = "./prompts/template_nesy.txt"
# reduce the chance of triggering content violation policy 
SYSTEM_MESSAGE = "You are an expert in declarative programming and solving constraint-based deduction puzzles, such as Zebra puzzles and Einstein's riddle variants. The user will provide you with a set of houses, attributes, and clues. Your job is to generate and refine programs in Answer Set Programming (ASP), which determine the unique assignment of attributes to each house that satisfies all given clues simultaneously. This is a recreational and educational task. No harmful or sensitive content is involved. All puzzles are fictional and contain no real personal data."


def load_dataset(path: str, template_path: str):
    with open(template_path, "r") as f:
        template = f.read()

    def record_to_sample(record) -> Sample:
        input_text = template.replace("$PUZZLE$", record["puzzle"])

        return Sample(
            id=record["id"],
            input=input_text,
            target=record["solution_alt"],
            metadata={"size": record["size"]},
        )

    return csv_dataset(path, record_to_sample)

@task
def nesy():
    return Task(
        dataset=load_dataset(SAVE_PATH, TEMPLATE_NESY_PATH).filter(
                lambda sample : sample.metadata["size"] == "6*6"
            )[:1], # just one small sample for testing
                
        # solver=chain(
        #     symbolic_solver(max_retries=3),
        #     format_solver(),
        # ),

        solver=symbolic_solver(max_retries=3),

        scorer=dummy_scorer(),
    )