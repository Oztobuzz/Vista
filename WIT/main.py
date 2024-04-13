from datasets import load_dataset

dataset = load_dataset("google/wit")

# Filter language to Vietnamese
dataset = dataset.filter(lambda example: example["language"] == "vi")

print(len(dataset))