from clingo import Control

from utils_clingo import validate_and_execute

"""
This file is for testing the utils_clingo functions in a standalone way, without the rest of the inspect_ai framework. It executes tests/test_clingo.lp. 

Usage: 

```
# from root directory
python -m tests.test_clingo
```

How does raw error msg look like: 

    --- syntax error ---

    <block>:16:1-6: error: syntax error, unexpected <IDENTIFIER>

    --- unsafe variable ---

    <block>:23:1-38: error: unsafe variables in:
    1<=#count{0,assigned_name(H,D):assigned_name(H,D):name(N)}<=1
    <block>:23:22-23: note: 'D' is unsafe

    --- error in aggregates --- 
    <block>:25:42-43: info: global variable in tuple of aggregate element:
    N

    --- multiple models ---
    <ERR_MULTIMODEL>

    --- unsat ---
    <ERR_UNSAT>

"""

if __name__ == "__main__":
    # this sample program has 2 stable models (if parsing success), which is not desired 
    # should stop as far as clingo finds the 2nd model, an report error 
    with open("tests/test_clingo.lp", "r") as f:
        program = f.read()

    correct, err, models = validate_and_execute(program)


    print("Correct:", correct)
    print("Error message:", err)
    if correct: 
        print("Models:", models[0])

