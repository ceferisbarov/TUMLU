from datasets import load_dataset

def drop_fifth(row):
    choices, answer = row["choices"], row["answer"]

    if len(choices) <= 4:
        return row

    if answer in "ABCD":  # Simply drop the 5th choice
        choices = choices[:4]
    elif answer == "E":  # Swap 4 and 5, drop the new 5, and update the answer
        choices[3], choices[4] = choices[4], choices[3]
        choices = choices[:4]
        answer = "D"

    row["choices"] = choices
    row["answer"] = answer

    return row

dataset = load_dataset("jafarisbarov/AzerbaijaniMMLU-small", download_mode="force_redownload")
subjects = list(set(dataset["dev"]["subject"]))

for subject in list(set(subjects)):
    subject_subset = dataset.filter(lambda x: x["subject"] == subject)
    dev_subset = subject_subset["dev"]
    test_subset = subject_subset["test"]
    dev_subset = dev_subset.map(drop_fifth)
    test_subset = test_subset.map(drop_fifth)
    dev_subset.to_json(f"./data/azerbaijani/dev/{subject}.jsonl", force_ascii=False)
    test_subset.to_json(f"./data/azerbaijani/test/{subject}.jsonl", force_ascii=False)
