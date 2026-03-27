# About 
This is the course project of "Reasoning with Large Language Models" at University of Potsdam. It evaluates LLMs on a small subset of the ZebraLogic benchmark [1], with two different approaches: 
* One-shot Chain-of-Thoughts (CoT) as the ZebraLogic paper [1], and 
* Neural-Symbolic integration with automatic refinement loop as in the paper DSPy-based neural-symbolic pipeline to enhance spatial reasoning in LLMs [2]

We leverage Inspect AI, a light-weighted LLM evaluation framework as the backbone. This way, we only need to implement data pre-processing, the Solver (meaning how we prompt the LLM in Inspect AI's terminologies), and the Scorer. 

# Prerequisite 
env variables (openai, HF, openrouter)
packages (Inspect AI, Hugging Face, openai)

# Files 



# Report Idea 
compare score 
compare score VS token 
compare score VS time 


# Development Process
Make sure things work with a free model: 
```
inspect eval eval_nesy.py --model openrouter/nvidia/nemotron-3-super-120b-a12b:free
```

Make sure we have proper difficulty levels: 
(one instance per level)
```
inspect eval eval_nesy.py --model openai/gpt-5.4
inspect eval eval_nesy.py --model openai/o3-2025-04-16
inspect eval eval_nesy.py --model openai/gpt-4.1-2025-04-14

inspect eval sample.py --model openrouter/deepseek/deepseek-v3.2

```
