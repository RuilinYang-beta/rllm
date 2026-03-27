from inspect_ai import task, Task
from inspect_ai import Task, task
from inspect_ai.solver import  system_message

from scorers import max_cell_match
from subset_data import SAVE_PATH
from solvers import symbolic_solver, format_solver
from utils import Content, load_dataset
from constants import TEMPLATE_NESY_PATH, SYSTEM_MESSAGE_PATH


@task
def nesy():
    return Task(
        dataset=load_dataset(SAVE_PATH, TEMPLATE_NESY_PATH),
                
        solver=[
            system_message(Content(SYSTEM_MESSAGE_PATH)),
            # auto-refinement loop, each row invokes clingo in a subprocess 
            symbolic_solver(max_retries=3),
            # format clingo stable model to JSON for scorer 
            format_solver(),
        ],

        scorer=max_cell_match(),
    )