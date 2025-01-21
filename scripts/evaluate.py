import os
import re
import json

from utils import get_acc

LANGUAGE = "crimean-tatar"
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
MODEL_NAME = "meta-llama/Meta-Llama-3.1-8B-Instruct"
# MODEL_NAME = "gpt-4o-2024-11-20"


def evaluate(language=LANGUAGE, model=MODEL_NAME):
    base_path = f"data/{language}/outputs/no_cot_instruct/{model}/"

    for subject in os.listdir(base_path):
        path = base_path + subject
        if not os.path.exists(path):
            continue

        with open(path, "r") as f:
            data = json.load(f)
            print(f"{subject[:-5]}: {100 * round(get_acc(data, language), 4)}")


if __name__ == "__main__":
    evaluate(LANGUAGE, MODEL_NAME)
