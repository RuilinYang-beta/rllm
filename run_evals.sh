#!/usr/bin/env bash

FILES=(
    "eval_cot.py"
    "eval_nesy.py"
)

# Models with no extra flags
MODELS=(
    "openai/gpt-4.1-2025-04-14"
)

# for file in "${FILES[@]}"; do
#     inspect eval "$file" --model openrouter/deepseek/deepseek-v3.2 -M "reasoning_enabled=true" 
# done

# Models with per-model reasoning effort levels
declare -A MODEL_EFFORTS
MODEL_EFFORTS["openai/o3-2025-04-16"]="low high"
MODEL_EFFORTS["openai/gpt-5.4"]="none xhigh"

# Models with on/off reasoning enabled
declare -A REASONING_ENABLED
REASONING_ENABLED["openrouter/deepseek/deepseek-v3.2"]="true false"

# Run standard models
# for file in "${FILES[@]}"; do
#     for model in "${MODELS[@]}"; do
#         inspect eval "$file" --model "$model"
#     done
# done

# # Run models with reasoning effort variants
# for file in "${FILES[@]}"; do
#     for model in "${!MODEL_EFFORTS[@]}"; do
#         for effort in ${MODEL_EFFORTS[$model]}; do
#             inspect eval "$file" --model "$model" --reasoning-effort "$effort"
#         done
#     done
# done

for file in "${FILES[@]}"; do
    for model in "${!REASONING_ENABLED[@]}"; do
        for switch in ${REASONING_ENABLED[$model]}; do
            inspect eval "$file" --model "$model" -M reasoning_enabled="$switch"
        done
    done
done