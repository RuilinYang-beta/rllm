import os
from dotenv import load_dotenv
from datasets import load_dataset, concatenate_datasets, load_from_disk

PLACEHOLDER = "___"
TARGET_SIZES = ["2*4", "3*4", "4*5", "5*6"]
SAMPLE_PER_SIZE = 8
SEED = 42
SAVE_PATH = "./data/small_dataset/"

# transform solution format to stay consistent with the CoT prompt in ZebraLogic paper
def add_solution_alt(row): 
    s_alt = {
        "reasoning": PLACEHOLDER, 
        "solution": {}
    }
    s = row['solution'] 
    for r in s['rows']: 
        s_alt['solution'][f'House {r[0]}'] = {}
        for attr in s['header'][1:]: 
            s_alt['solution'][f'House {r[0]}'][attr] = PLACEHOLDER

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


    small_dataset = small_dataset.map(add_solution_alt)

    small_dataset.save_to_disk(SAVE_PATH)
    print(f"Saved {len(small_dataset)} rows to {SAVE_PATH}")


def test(): 
    ds = load_from_disk(SAVE_PATH)
    print(f"Loaded local dataset:\n{repr(ds)}")


if __name__ == "__main__":
    main()
    # test()



