from typing import Tuple

from inspect_ai.solver._task_state import TaskState
from inspect_ai.scorer._target import Target
from inspect_ai.scorer._metric import CORRECT, INCORRECT, Score
from inspect_ai.scorer._scorer import Scorer, scorer 
from inspect_ai.scorer._metrics import mean, stderr

from utils import str_to_dict


# for dev purpose 
@scorer(metrics=[mean(), stderr()])
def dummy_scorer() -> Scorer:

    async def score(state: TaskState, target: Target) -> Score: 
        return Score(
            value=CORRECT,  
            answer=state.output.completion, 
        )

    return score

def max_cell_match_helper(ans_dict: dict, tar_dict: dict) -> Tuple[int, str]:
    total_match = 0
    explanation = ""
    
    for key in tar_dict['solution'].keys(): 
        if key not in ans_dict['solution']: 
            explanation = f"Key \"{key}\" missing, skip. \n{explanation}"
            continue
        
        # be very lenient, the Attr name is not standardized, 
        # don't penalize over that as long as the values are the same as a set
        tar_set = set(tar_dict['solution'][key].values())
        ans_set = set(ans_dict['solution'][key].values())
    
        cell_match = len(tar_set.intersection(ans_set))
        total_match += cell_match

        if cell_match < len(tar_set): 
            explanation = f"For {key},\n- {cell_match} attrs are correct;\n- these attrs should be in answer but are not: {tar_set - ans_set} \n{explanation}"
        
    return total_match, explanation


def count_total_cells(d: dict) -> int: 
    total = 0
    for key in d: 
        if key != "reasoning": 
            if isinstance(d[key], dict): 
                total += count_total_cells(d[key])
            else: 
                total += 1
    return total

@scorer(
        metrics={
            "table_match": [mean(), stderr()],
            "cells_match_ratio": [mean(), stderr()]
        }
)
def max_cell_match() -> Scorer: 

    async def score(state: TaskState, target: Target) -> Score: 
        ans_dict = str_to_dict(state.output.completion)
        tar_dict = str_to_dict(target.text)

        if "solution" not in ans_dict: 
            return Score(
                value={"table_match": INCORRECT, "cells_match_ratio": 0},
                answer=state.output.completion, 
                explanation="Key 'solution' not in answer"
            )
        else: 
            cell_match, explanation = max_cell_match_helper(ans_dict, tar_dict)

        total = count_total_cells(tar_dict['solution'])

        return Score(
            value={
                    "table_match": 1 if cell_match == total and total > 0 else 0,
                    "cells_match_ratio": float(cell_match / total) if total > 0 else 0, 
                },  
            answer=state.output.completion, 
            explanation=explanation
        )

    return score


def max_dict_equal_test(): 

    d1 = str_to_dict("""{'reasoning': '___', 'solution': '{"House 1":{"Name":"Eric","Height":"short","Hobby":"gardening","Food":"pizza","Occupation":"engineer"},"House 2":{"Name":"Arnold","Height":"very short","Hobby":"photography","Food":"grilled cheese","Occupation":"doctor"}}'}""")
    
    d1_reorder = str_to_dict("""{'reasoning': '___', 'solution': '{"House 1":{"Name":"Eric","Hobby":"gardening","Food":"pizza","Height":"short","Occupation":"engineer"},"House 2":{"Height":"very short","Hobby":"photography","Food":"grilled cheese","Occupation":"doctor","Name":"Arnold"}}'}""")
    
    # changed 1 cell compared to d1
    d2 = str_to_dict("""{'reasoning': '___', 'solution': '{"House 1":{"Name":"Eric","Height":"short","Hobby":"gardening","Food":"pizza","Occupation":"alien_warrior"},"House 2":{"Name":"Arnold","Height":"very short","Hobby":"photography","Food":"grilled cheese","Occupation":"doctor"}}'}""")

    total_cells = count_total_cells(d1)

    assert max_cell_match_helper(d1, d1_reorder) == (total_cells, "")
    assert max_cell_match_helper(d1, d2)[0] == total_cells - 1


if __name__ == "__main__":
    max_dict_equal_test()