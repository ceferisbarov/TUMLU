from glob import glob
import json
import os
from tqdm import tqdm
from umsc import UgMultiScriptConverter

source_script = 'UAS'
target_script = 'ULS'
converter = UgMultiScriptConverter(source_script, target_script)

input_paths = glob("data/uyghur/*/*.jsonl")
os.makedirs("data/uyghur-latin/dev/", exist_ok=True)
os.makedirs("data/uyghur-latin/test/", exist_ok=True)
for input_path in tqdm(input_paths):
    output_path = input_path.replace("uyghur/", "uyghur-latin/")

    with open(input_path, "r") as f1, open(output_path, "w") as f2:
        for line in f1.readlines():
            data = json.loads(line)
            data["question"] = converter(data["question"])
            data["choices"] = [converter(choice) for choice in data["choices"]]

            json.dump(data, f2, ensure_ascii=False)
