from datasets import load_dataset

dataset = None

def get_squad_examples(limit=100):
    global dataset

    if dataset is None:
        dataset = load_dataset("squad", split="train")

    examples = []

    for i in range(limit):
        item = dataset[i]

        examples.append({
            "context": item["context"],
            "question": item["question"],
            "answer": item["answers"]["text"][0] if item["answers"]["text"] else ""
        })

    return examples