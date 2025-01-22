from datasets import load_dataset, Dataset

dataset = load_dataset("jafarisbarov/UyghurMMLU", download_mode="force_redownload")[
    "train"
]
subjects = list(set(dataset["subject"]))

for subject in list(set(subjects)):
    subset = dataset.filter(lambda x: x["subject"] == subject)
    Dataset.from_dict(subset[:5]).to_json(
        f"./data/uyghur/dev/{subject}.jsonl", force_ascii=False
    )
    Dataset.from_dict(subset[5:]).to_json(
        f"./data/uyghur/test/{subject}.jsonl", force_ascii=False
    )
