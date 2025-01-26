import os
import json
from itertools import product
import pandas as pd

from utils import LANGUAGES, MODEL_NAMES, get_acc

results = pd.DataFrame({"language": [], "model": [], "subject": [], "accuracy": []})
for pair in product(LANGUAGES, MODEL_NAMES):
    language, model = pair
    base_path = f"data/{language}/outputs/no_cot_instruct/{model}/"

    if not os.path.exists(base_path):
        continue
    for subject in os.listdir(base_path):
        path = base_path + subject
        if not os.path.exists(path):
            results.loc[results.shape[0] + 1] = (language, model, subject.lower(), None)
            continue

        with open(path, "r") as f:
            data = json.load(f)
        accuracy = 100 * round(get_acc(data, language), 4)
        results.loc[results.shape[0] + 1] = (language, model, subject.lower(), accuracy)

results.to_csv("results.csv", index=False)
