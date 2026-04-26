from datasets import load_dataset

dataset = None

def get_dataset():
    global dataset
    if dataset is None:
        dataset = load_dataset("squad")
    return dataset