import os
import json
import pandas as pd
from datasets import Dataset

data = []
with open("data/uzbek-cyrillic/data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data.append(json.loads(line))

ds = Dataset.from_pandas(pd.DataFrame(data=data))

for subject in set(ds["subject"]):
    # dev_path = os.path.join("dev", subject + ".jsonl")
    test_path = "data/uzbek-cyrillic/test/" + subject + ".jsonl"
    test_split = ds.filter(lambda x: x["subject"] == subject)
    print(test_path)
    # with open(test_path, "w") as f:
    #     test_split.to_json(test_path, force_ascii=False)
