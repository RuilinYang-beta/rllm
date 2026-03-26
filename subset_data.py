import os
import pandas as pd
from pprint import pprint 
from dotenv import load_dotenv
from datasets import load_dataset, concatenate_datasets
from utils import str_to_dict

"""
This script load the original dataset from HuggingFace, sample a small subset of it, and save the subset to a local CSV file.
"""

PLACEHOLDER = "___"
# every upgrade of level: 
# search space -> 3, 7, 12, 17
# z3 conflict -> 5, 16, 48, 97
TARGET_SIZES = ["3*4", "4*5", "5*6", "6*6"]
SAMPLE_PER_SIZE = 5
SEED = 42
SAVE_PATH = "./data/small_dataset.csv"

# add a `solution_inst` and `solution_alt` column 
# that complies to the format in prompting template
# `solution_inst` is part of the prompt, and `solution_alt` should be the answer 
def process_solution(row): 
    s_inst = {
        "reasoning": PLACEHOLDER, 
        "solution": {}
    }
    s_alt = {
        "reasoning": PLACEHOLDER, 
        "solution": {}
    }    
    s = row['solution'] 
    for r in s['rows']: 
        s_inst['solution'][f'House {r[0]}'] = {}
        s_alt['solution'][f'House {r[0]}'] = {}
        
        for attr_idx in range(1, len(s['header'])):
            attr_name = s['header'][attr_idx]
            s_inst['solution'][f'House {r[0]}'][attr_name] = PLACEHOLDER
            s_alt['solution'][f'House {r[0]}'][attr_name] = r[attr_idx]
            
    row['solution_inst'] = s_inst
    row['solution_alt'] = s_alt
    return row

def sample_by_size(ds, sizes, sample_per_size, seed): 
    subsets = []

    for size in sizes:
        filtered = ds.filter(lambda x: x["size"] == size)
        sampled = filtered.shuffle(seed=seed).select(range(sample_per_size))
        subsets.append(sampled)

    return concatenate_datasets(subsets)

def main(): 
    # load HuggingFace token `HF_READ_TOKEN` from env 
    load_dotenv()

    ds = load_dataset("allenai/ZebraLogicBench-private", "grid_mode", 
                    split='test', 
                    token=os.getenv("HF_READ_TOKEN"))

    small_dataset = sample_by_size(ds, TARGET_SIZES, SAMPLE_PER_SIZE, SEED)


    small_dataset = small_dataset.map(process_solution)

    small_dataset.to_csv(SAVE_PATH, index=False)

    # small_dataset.save_to_disk(SAVE_PATH)
    print(f"Saved {len(small_dataset)} rows to {SAVE_PATH}")


def test():

    df = pd.read_csv(SAVE_PATH)

    print(df['solution'].iloc[0])
    
    for col in ['solution_inst', 'solution_alt']: 
        value = df[col].iloc[0]
        parsed = str_to_dict(value)

        pprint(parsed, indent=2)


if __name__ == "__main__":
    # main()

    test()



