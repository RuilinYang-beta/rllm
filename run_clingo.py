import sys
import json
from clingo import Control, MessageCode
from constants import ERR_UNSAT, ERR_MULTIMODEL

def main():
    program = sys.stdin.read()
    messages = []

    def logger(code: MessageCode, message: str):
        messages.append(message)

    try:
        ctl = Control(["--models=2"], logger=logger, message_limit=20)
        ctl.add("base", [], program)
        ctl.ground([("base", [])])
    except RuntimeError:
        error_msg = "\n".join(messages) if messages else "Unknown grounding error."
        print(json.dumps({"ok": False, "error": error_msg}))
        return

    models = []

    def on_model(m):
        models.append([str(s) for s in m.symbols(shown=True)])
        if len(models) >= 2:  # correct program should have one and only one stable model
            return False

    solve_result = ctl.solve(on_model=on_model)

    if solve_result.unsatisfiable:
        print(json.dumps({"ok": False, "error": ERR_UNSAT}))
    elif len(models) > 1:
        print(json.dumps({"ok": False, "error": ERR_MULTIMODEL}))
    else:
        print(json.dumps({"ok": True, "models": models}))

if __name__ == "__main__":
    main()