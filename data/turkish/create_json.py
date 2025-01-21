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


for subject in subjects:
    dataset = load_dataset("AYueksel/TurkishMMLU", subject)
    dev_subset = dataset["dev"]
    test_subset = dataset["test"]
    dev_subset = dev_subset.map(drop_fifth)
    test_subset = test_subset.map(drop_fifth)
    dev_subset.to_json(f"./data/turkish/dev/{subject}.jsonl", force_ascii=False)
    test_subset.to_json(f"./data/turkish/test/{subject}.jsonl", force_ascii=False)
