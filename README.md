Make sure things work with a free model: 
```
inspect eval eval_nesy.py --model openrouter/nvidia/nemotron-3-super-120b-a12b:free
```

Make sure we have proper difficulty levels: 
(one instance per level)
```
inspect eval eval_nesy.py --model openai/gpt-5.4
inspect eval sample.py --model anthropic/claude-opus-4-6
inspect eval sample.py --model openrouter/deepseek/deepseek-v3.2

```
