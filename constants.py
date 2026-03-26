

TEMPLATE_COT_PATH = "./prompts/template_cot.txt"
SYSTEM_MESSAGE_PATH = "./prompts/system_cot.txt"

TEMPLATE_NESY_PATH = "./prompts/template_nesy.txt"
SYSTEM_MESSAGE_PATH = "./prompts/system_nesy.txt"

# used in the 2nd phase of nesy, reformatting stable models to JSON 
FORMAT_INSTRUCTION_PATH = "./prompts/format_nesy.txt"

# used to give LLM feedback based on error messages from clingo
ERR_UNSAT = "Error: UNSAT."
ERR_MULTIMODEL = "Error: MultiModels."
FEEDBACK_BASE_PATH = "feedback_messages/"