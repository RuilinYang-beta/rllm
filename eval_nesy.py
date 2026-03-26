from inspect_ai import task, Task
from inspect_ai import Task, task
from inspect_ai.solver import  system_message

from scorers import max_cell_match, dummy_scorer
from subset_data import SAVE_PATH, DEV_SAVE_PATH
from solvers import symbolic_solver, format_solver

from eval_cot import load_dataset
from utils import Content

TEMPLATE_NESY_PATH = "./prompts/template_nesy.txt"
# reduce the chance of triggering content violation policy 
SYSTEM_MESSAGE_PATH = "./prompts/system_nesy.txt"


@task
def nesy():
    return Task(
        dataset=load_dataset(SAVE_PATH, TEMPLATE_NESY_PATH).filter(
                lambda sample : sample.metadata["size"] == "6*6"
            )[:1], # just one sample for testing
                
        solver=[
            system_message(Content(SYSTEM_MESSAGE_PATH)),
            symbolic_solver(max_retries=3),
            format_solver(),
        ],

        scorer=max_cell_match(),
    )