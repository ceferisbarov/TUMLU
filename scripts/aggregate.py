import os
import json

LANGUAGE = "uzbek"
MODEL_NAME = "google/gemma-2-27b-it"


def get_acc(data):
    for i in data:
        if "A)" in i["output"]:
            i["prediction"] = "A"
        elif "B)" in i["output"]:
            i["prediction"] = "B"
        elif "C)" in i["output"]:
            i["prediction"] = "C"
        elif "D)" in i["output"]:
            i["prediction"] = "D"
        else:
            i["prediction"] = None

    if len(data):
        return sum(map(lambda x: x["prediction"] == x["answer"], data)) / len(data)

    return 0


base_path = f"data/{LANGUAGE}/outputs/no_cot_instruct/{MODEL_NAME}/"

for subject in os.listdir(base_path):
    # path = f"outputs_shuffled/no_cot_instruct/{MODEL_NAME}/{subject}.json"
    path = base_path + subject
    if not os.path.exists(path):
        continue

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(path)
            print(e)
        print(f"{subject[:-5]}: {100 * round(get_acc(data), 4)}")
