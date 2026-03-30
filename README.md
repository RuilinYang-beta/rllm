# Quick Note
The project is complete but the file structure is a bit messy. I'd clean it up and verify everything still works, but VPN issues prevent verifying + committing to GitHub — so the structure stays as-is. Uploading this README via browser is the only option now, so the description below reflects the current working state.

# About 
This is the course project of "Reasoning with Large Language Models" at University of Potsdam. It evaluates LLMs on a small subset of the ZebraLogic benchmark [1], with two different approaches: 
* One-shot Chain-of-Thoughts (CoT) as the ZebraLogic paper [1], and 
* Neural-Symbolic integration with automatic refinement loop as in the paper DSPy-based neural-symbolic pipeline to enhance spatial reasoning in LLMs [2]

We leverage Inspect AI[3], a light-weighted LLM evaluation framework as the backbone. This way, we only need to implement data pre-processing, the Solver (meaning how we prompt the LLM in Inspect AI's terminologies), and the Scorer. 

# Prerequisite 
## Packages 
The dependencies are listed in `requirements.txt`. 
After installing Inspect AI, the results in `./logs` is viewable with the command `inspect view`.  


## Environment variables
The following environment variables need to be set, exactly under these names: 
```
# OpenAI API key 
# (must have, for running the models)
OPENAI_API_KEY=...

# HuggingFace token for read access 
# (optional, only if want to process data from the source) 
HF_TOKEN=...

# OpeneRouter API key
(optional, only if want to test the pipeline with free openrouter model)
OPENROUTER_API_KEY=...
```

# Files 
## Entry points
* `./run_eval.sh`
    - Invoke model evaluation on the same dataset. 
* `./run_rescore.sh`
    - re-score existing evaluation logs, used when there's changes in the scorers, but a complete re-run is not necessary.     
* `eval_cot.py`
    - Prompt the model in chain-of-thoughts fashion; 
    - each puzzle is inserted to CoT template on-the-fly, with the instruction of formatting the answer in a JSON object;
    - the solver (Inspect AI's terminologies, meaning how we prompt the LLM) is the built-in `generate` of Inspect AI, meaning it's just a plain API call
    - the scorer `max_cell_match` compares the JSON result with the gold solution at cell level 
* `eval_nesy.py`
    - Prompt the model in the neural-symbolic pipeline: 
        - each puzzle is inserted to Nesy template on-the-fly to generate a valid ASP program;
        - the solver `symbolic_solver` takes care of the auto-refinement loop, till a valid ASP program is generated; or till `max_retries` is exhausted;
        - the clingo stable model is passed to the solver `format_solver`, to be converted to JSON format for automatic scoring 
        - the scorer `max_cell_match` compares the JSON result with the gold solution at cell level 

## Prompting and Scoring 
* `solvers.py`
    - `symbolic_solver`: in a subprocess, invoke clingo and run the script in `run_clingo.py` (because Inspect AI framework run all the testing instances concurrently, we want to make it non-blocking as possible), try parsing and solving the generated ASP program; give feedbacks on parsing errors, as well as semantic errors (e.g. when the ASP program is unsatisfiiable, or has more than 1 stable model)
    -  `format_solver`: instruct the LLM to convert clingo output into JSON format
* `scorers.py`: 
    - `max_cell_match`: recursively compare the JSON object from the model, with the gold solution; return the cell match ratio, and a brief summary of where the non-matches happen. 

## Other files 
* Data: 
    - `subset_data.py`: extract a small subset of ZebraLogic from HuggingFace; only need to be run once.
    - `./data/`: directory containing the subset we use. 
* Utils: small util functions / variables 
    - `utils.py`
    - `constants.py` 
* Prompts: 
    - `./prompts/`: system prompts, normal prompts 
    - `./feedback_messages/`: feedback messages per error type in Nesy pipeline 
* `./logs/`: Evaluation results 
* `./analysis/`: Analysis of the results     
* `./tests/`: a standalone ASP program, and a script to test it 

# References 
[1] Lin, Bill Yuchen, et al. "Zebralogic: On the scaling limits of llms for logical reasoning." arXiv preprint arXiv:2502.01100 (2025).
[2] Wang, Rong, and Kun Sun. "DSPy-based neural-symbolic pipeline to enhance spatial reasoning in LLMs." Neural Networks (2025): 108022.
[3] AI Security Institute, UK. Inspect AI: Framework for Large Language Model Evaluations. May 2024, https://github.com/UKGovernmentBEIS/inspect_ai