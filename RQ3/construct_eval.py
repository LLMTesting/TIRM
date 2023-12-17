import json
import random
import tqdm

random.seed(43)

def load_dataset(path: str):
    print("loading dataset")
    with open(path, "r", encoding="utf-8") as f:
        objs = json.loads(f.read())
    
    return objs

dataset_out = []
dataset = load_dataset("retrain_valid.json")


# single round
dataset_out.extend(dataset)

# prompt
for obj in tqdm.tqdm(dataset):
    conversations = obj["conversations"]