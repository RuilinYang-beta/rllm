from inspect_ai import Task
from inspect_ai.solver import solver
from inspect_ai.solver._task_state import TaskState
from inspect_ai.model import ChatMessageUser

from utils_clingo import validate_and_execute, make_feedback_message, ClingoSubprocessError
from utils import Content
from constants import FORMAT_INSTRUCTION_PATH


@solver
def symbolic_solver(max_retries: int = 3):
    async def solve(state: TaskState, generate) -> TaskState:
        attempt = 0

        while attempt < max_retries + 1:
            state = await generate(state)
            
            if state.completed and state.output.stop_reason != "stop":
                state.metadata["failed"] = True
                return state

            symbolic_output = state.output.completion

            try:
                is_valid, error_msg, result = await validate_and_execute(symbolic_output)
            except ClingoSubprocessError as e:
                # Infrastructure failure — abort immediately, don't retry
                state.metadata["failed"] = True
                state.metadata["infra_error"] = str(e)
                return state

            if is_valid:
                state.metadata["execution_result"] = result[0]
                return state
            else: 
                attempt += 1
                feedback = make_feedback_message(error_msg)
                state.messages.append(ChatMessageUser(content=feedback))

        # Retries exhausted
        state.metadata["execution_result"] = None
        state.metadata["failed"] = True
        return state

    return solve


@solver
def format_solver():
    async def solve(state: TaskState, generate) -> TaskState:
        if state.metadata.get("failed") or not state.metadata.get("execution_result"):
            return state

        result = state.metadata["execution_result"]
        result_str = f"{'.\n'.join(str(atom) for atom in result)}."

        prompt = (
            f"The ASP solver produced the following stable model:\n\n"
            f"{result_str}\n\n"
            f"{Content(FORMAT_INSTRUCTION_PATH)}"
        )

        state.messages.append(ChatMessageUser(content=prompt))
        state = await generate(state)


        return state

    return solve