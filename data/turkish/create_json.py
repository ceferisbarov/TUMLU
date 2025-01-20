from datasets import load_dataset

subjects = [
    "Biology",
    "Chemistry",
    "Geography",
    "Chemistry",
    "History",
    "Mathematics",
    "Philosophy",
    "Physics",
    "Religion_and_Ethics",
    "Turkish_Language_and_Literature",
]

for subject in subjects:
    dataset = load_dataset("AYueksel/TurkishMMLU", subject)
    dev_subset = dataset["dev"]
    test_subset = dataset["test"]
    dev_subset.to_json(f"./data/turkish/dev/{subject}.jsonl", force_ascii=False)
    test_subset.to_json(f"./data/turkish/test/{subject}.jsonl", force_ascii=False)
