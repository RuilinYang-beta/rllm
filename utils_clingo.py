import json 
from inspect_ai.util import subprocess as inspect_subprocess

from clingo import Control, MessageCode
from utils import Content
from constants import FEEDBACK_BASE_PATH, ERR_UNSAT, ERR_MULTIMODEL

class ClingoSubprocessError(Exception):
    """Raised when the clingo subprocess itself fails, not due to the ASP program."""
    pass

def parse_and_ground(program: str) -> tuple[Control | None, str | None]:
    """
    Args: program: ASP program as a string
    Returns: (ctl, error_msg) — ctl is None on failure.
    """
    messages = [] 

    def logger(code: MessageCode, message: str) -> None:
        messages.append(message)

    try: 
        ctl = Control(["--models=2"], logger=logger, message_limit=20)
        ctl.add("base", [], program)
        ctl.ground([("base", [])])
        return ctl, None
    except RuntimeError as e:
        error_msg = "\n".join(messages) if messages else "Unknown grounding error."
        return None, error_msg



def solve(ctl: Control) -> tuple[bool, str, list | None]:
    """
    Solve and enforce exactly-one-stable-model semantics.
    Returns:
        correct: whether the program is valid and has exactly one stable model
        error_msg: if not valid, the error message to provide feedback
        models: list of lists, where each inner list is the atoms in a stable model; None on failure
    """
    correct = False
    error_msg = ""
    models = []

    def on_model(m):
        symbols = [str(s) for s in m.symbols(shown=True)]
        models.append(symbols)

        if len(models) >= 2:
            return False

    solve_result = ctl.solve(on_model=on_model)

    if solve_result.unsatisfiable:
        error_msg = ERR_UNSAT # No stable model exists."
    elif len(models) > 1:
        error_msg = ERR_MULTIMODEL # Expected exactly one stable model, but found at least two."
    else:
        correct = True

    return correct, error_msg, models

# def validate_and_execute(program: str) -> tuple[bool, str, list | None]:
#     """
#     Public interface expected by symbolic_solver.
#     Returns (is_valid, error_msg, atoms).
#     """
#     ctl, error_msg = parse_and_ground(program)
#     if error_msg:
#         return False, error_msg, None

#     return solve(ctl)

async def validate_and_execute(program: str) -> tuple[bool, str, list | None]:
    """
    Async-safe public interface for symbolic_solver.
    Runs clingo in a subprocess managed by Inspect's concurrency system.
    Returns (is_valid, error_msg, models).
    """
    try:
        result = await inspect_subprocess(
            ["python", "run_clingo.py"],
            input=program,
            timeout=30,
        )
    except TimeoutError:
        raise ClingoSubprocessError("Clingo subprocess timed out.")

    if not result.success:
        raise ClingoSubprocessError(f"Clingo subprocess failed: {result.stderr}")

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ClingoSubprocessError(f"Malformed JSON from clingo: {result.stdout!r}")

    if data["ok"]:
        return True, "", data["models"]
    else:
        return False, data["error"], None


def make_feedback_message(error_msg: str) -> str:
    if "syntax error" in error_msg:
        return Content(f"{FEEDBACK_BASE_PATH}/syntax_error.txt", error_msg)
    elif "unsafe" in error_msg:
        return Content(f"{FEEDBACK_BASE_PATH}/unsafe_variable.txt", error_msg)
    elif "aggregate" in error_msg:
        return Content(f"{FEEDBACK_BASE_PATH}/aggregate_misuse.txt", error_msg)
    elif ERR_UNSAT in error_msg:
        return Content(f"{FEEDBACK_BASE_PATH}/err_unsat.txt", error_msg)
    elif ERR_MULTIMODEL in error_msg:
        return Content(f"{FEEDBACK_BASE_PATH}/err_multimodel.txt", error_msg)
    else: 
        return Content(f"{FEEDBACK_BASE_PATH}/unknown_error.txt")
