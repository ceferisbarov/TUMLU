from datasets import load_dataset

dataset = load_dataset("jafarisbarov/UzbekMMLU", download_mode="force_redownload")[
    "train"
]

subjects = list(set(dataset["subject"]))

for subject in list(set(subjects)):
    dataset.filter(lambda x: x["subject"] == subject).to_json(
        f"{subject}.jsonl", force_ascii=False
    )
