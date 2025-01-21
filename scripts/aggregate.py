import os
import re
import json
from itertools import product
import pandas as pd

from evaluate import get_acc

LANGUAGES = [
    "azerbaijani",
    "crimean-tatar",
    "karakalpak",
    "kazakh",
    "tatar",
    "turkish",
    "uzbek",
    "uyghur",
]

MODEL_NAMES = [
    "claude-3-5-sonnet-v2@20241022",
    "claude-3-5-haiku@20241022",
    "gpt-4o-2024-11-20",
    "Qwen/Qwen2.5-7B-Instruct",
    #    "Qwen/Qwen2.5-32B-Instruct", Doesn't exist in DeepInfra
    "Qwen/Qwen2.5-72B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "gemini-1.5-flash",
    # "gemini-2.0-flash", # not supported?
    "gemini-1.5-pro",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
]

results = pd.DataFrame({"language": [], "model": [], "subject": [], "accuracy": []})
for pair in product(LANGUAGES, MODEL_NAMES):
    language, model = pair
    base_path = f"data/{language}/outputs/no_cot_instruct/{model}/"

    if not os.path.exists(base_path):
        continue
    for subject in os.listdir(base_path):
        path = base_path + subject
        if not os.path.exists(path):
            continue

        with open(path, "r") as f:
            data = json.load(f)
            accuracy = 100 * round(get_acc(data, language), 4)

        # results.append(language, model, subject, accuracy)
        results.loc[results.shape[0] + 1] = (language, model, subject.lower(), accuracy)

results.to_csv("results.csv", index=False)
