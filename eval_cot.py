from inspect_ai import Task, task
from inspect_ai.solver import generate, system_message

from scorers import max_cell_match
from subset_data import SAVE_PATH
from utils import Content, load_dataset
from constants import TEMPLATE_COT_PATH, SYSTEM_MESSAGE_PATH


@task
def naive_cot():
    return Task(
        dataset=load_dataset(SAVE_PATH, TEMPLATE_COT_PATH),
        solver=[system_message(Content(SYSTEM_MESSAGE_PATH)), generate()],
        scorer=max_cell_match(),
    )