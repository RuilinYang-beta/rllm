from clingo import Control, MessageCode

ERR_UNSAT = "Error: UNSAT."
ERR_NOMODEL = "Error: NoModels."
ERR_MULTIMODEL = "Error: MultiModels."

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
        is_valid: whether the program is valid and has exactly one stable model
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
    elif len(models) == 0:
        error_msg = ERR_NOMODEL # Solver returned SAT but no model was captured."
    elif len(models) > 1:
        error_msg = ERR_MULTIMODEL # Expected exactly one stable model, but found at least two."
    else:
        correct = True

    return correct, error_msg, models


if __name__ == "__main__":
    # this sample program has 2 stable models (if parsing success), which is not desired 
    # should stop as far as clingo finds the 2nd model, an report error 
    with open("tests/test_clingo.lp", "r") as f:
        program = f.read()

    ctl, error_msg = parse_and_ground(program)

    if error_msg:
        # in real solver: return (False, error_msg, None) -> reprompt 
        print("Error during parsing/grounding:", error_msg)
    else: 
        correct, err, models = solve(ctl)

        print("Correct:", correct)
        print("Error message:", err)
        print("Models:", models[0])


"""
How does raw error msg look like: 

--- syntax error ---

<block>:16:1-6: error: syntax error, unexpected <IDENTIFIER>

--- unsafe variable ---

<block>:23:1-38: error: unsafe variables in:
  1<=#count{0,assigned_name(H,D):assigned_name(H,D):name(N)}<=1
<block>:23:22-23: note: 'D' is unsafe


--- multiple models ---
<ERR_MULTIMODEL>

--- unsat ---
<ERR_UNSAT>

--- satisfiable but no model captured (shouldn't happen) ---
<ERR_NOMODEL>

"""