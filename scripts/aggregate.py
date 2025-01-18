import os
import json

LANGUAGE = "uzbek"
MODEL_NAME = "google/gemma-2-27b-it"

keyword_dict = {"uzbek": "Javob", "crimean-tatar": "Cevap", "tatar": "Җавап"}


def get_acc(data, language):
    keyword = keyword_dict[language]
    for i in data:
        if f"{keyword}: A" in i["output"]:
            i["prediction"] = "A"
            continue
        elif f"{keyword}: B" in i["output"]:
            i["prediction"] = "B"
            continue
        elif f"{keyword}: C" in i["output"]:
            i["prediction"] = "C"
            continue
        elif f"{keyword}: D" in i["output"]:
            i["prediction"] = "D"
            continue

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
    path = base_path + subject
    if not os.path.exists(path):
        continue

    with open(path, "r") as f:
        data = json.load(f)
        print(f"{subject[:-5]}: {100 * round(get_acc(data, LANGUAGE), 4)}")
