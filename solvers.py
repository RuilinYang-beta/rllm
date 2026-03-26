from inspect_ai import Task
from inspect_ai.solver import solver, chain, generate
from inspect_ai.solver._task_state import TaskState
from inspect_ai.model import ChatMessageUser

from utils_clingo import validate_and_execute, make_feedback_message

@solver
def symbolic_solver(max_retries: int = 3):
    async def solve(state: TaskState, generate) -> TaskState:
        attempt = 0

        while attempt < max_retries + 1:
            state = await generate(state)
            
            if state.completed:
                state.metadata["failed"] = True
                return state

            symbolic_output = state.output.completion
            is_valid, error_msg, result = validate_and_execute(symbolic_output)

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
        # Convert atom list to a readable string for the LLM
        result_str = "\n".join(str(atom) for atom in result)

        prompt = (
            f"The ASP solver produced the following stable model:\n\n"
            f"{result_str}\n\n"
            "Convert it to the required output format."
        )
        state.messages.append(ChatMessageUser(content=prompt))
        state = await generate(state)

        if state.completed:
            state.metadata["failed"] = True

        return state

    return solve