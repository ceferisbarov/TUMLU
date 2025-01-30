from datasets import load_dataset, Dataset

dataset = load_dataset(
    "jafarisbarov/CrimeanTatarMMLU-cyrillic", download_mode="force_redownload"
)[
    "test"
]  # train split is older. test split comes from the fork
# dataset = load_dataset("jafarisbarov/CrimeanTatarMMLU")["train"]

subjects = list(set(dataset["subject"]))

for subject in list(set(subjects)):
    subset = dataset.filter(lambda x: x["subject"] == subject)
    Dataset.from_dict(subset[:5]).to_json(
        f"./data/crimean-tatar-cyrillic/dev/{subject}.jsonl", force_ascii=False
    )
    Dataset.from_dict(subset[5:]).to_json(
        f"./data/crimean-tatar-cyrillic/test/{subject}.jsonl", force_ascii=False
    )
