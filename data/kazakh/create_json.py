from datasets import load_dataset, Dataset

dataset = load_dataset("jafarisbarov/KazakhMMLU", download_mode="force_redownload")

subjects = list(set(dataset["test"]["subject"]))

for subject in list(set(subjects)):
    dev_subset = dataset["dev"].filter(lambda x: x["subject"] == subject)
    test_subset = dataset["test"].filter(lambda x: x["subject"] == subject)
    test_subset = Dataset.from_dict(test_subset[:100])
    dev_subset.to_json(f"./data/kazakh/dev/{subject}.jsonl", force_ascii=False)
    test_subset.to_json(f"./data/kazakh/test/{subject}.jsonl", force_ascii=False)
