from inspect_ai.solver._task_state import TaskState
from inspect_ai.scorer._target import Target
from inspect_ai.scorer._metric import CORRECT, INCORRECT, Score
from inspect_ai.scorer._scorer import Scorer, scorer 

from utils import str_to_dict

def max_dict_equal(ans: dict, target: dict) -> bool:
    for key in target:
        if key != "reasoning": 
        
            if key not in ans: 
                return False 

            v1, v2 = ans[key], target[key]
            if isinstance(v1, dict) and isinstance(v2, dict):
                if not max_dict_equal(v1, v2):
                    return False
            elif v1 != v2:
                return False
    return True


@scorer
def max_dict_match() -> Scorer: 

    async def score(state: TaskState, target: Target) -> Score: 
        # check for correct
        ans_dict = str_to_dict(state.output.completion)
        tar_dict = str_to_dict(target.text)

        correct = (
            "solution" in ans_dict
            and max_dict_equal(ans_dict, tar_dict)
        )
        
        return Score(
            value = CORRECT if correct else INCORRECT,
            answer=state.output.completion
        )

    return score


def cell_match(): 
    pass 


def test(): 
    d1 = str_to_dict("""{'reasoning': '___', 'solution': '{"House 1":{"Name":"Eric","Height":"short","Hobby":"gardening","Food":"pizza","Occupation":"engineer"},"House 2":{"Name":"Arnold","Height":"very short","Hobby":"photography","Food":"grilled cheese","Occupation":"doctor"}}'}""")
    d1_reorder = str_to_dict("""{'reasoning': '___', 'solution': '{"House 1":{"Name":"Eric","Hobby":"gardening","Food":"pizza","Height":"short","Occupation":"engineer"},"House 2":{"Height":"very short","Hobby":"photography","Food":"grilled cheese","Occupation":"doctor","Name":"Arnold"}}'}""")
    
    d2 = str_to_dict("""{'reasoning': '___', 'solution': '{"House 1":{"Name":"Eric","Height":"short","Hobby":"gardening","Food":"pizza","Occupation":"alien_warrior"},"House 2":{"Name":"Arnold","Height":"very short","Hobby":"photography","Food":"grilled cheese","Occupation":"doctor"}}'}""")

    assert max_dict_equal(d1, d1_reorder)
    assert not max_dict_equal(d1, d2)


if __name__ == "__main__":
    test()