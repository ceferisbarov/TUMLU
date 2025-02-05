import os
import json
from itertools import product
import pandas as pd

from utils import LANGUAGES, MODEL_NAMES, get_acc

results = pd.DataFrame({"language": [], "model": [], "subject": [], "accuracy": []})
for pair in product(LANGUAGES, MODEL_NAMES):
    #  print(pair)
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


output_dir = 'results'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

results.to_csv(os.path.join(output_dir, "results.csv"), index=False)


# Convert accuracy to numeric, coercing errors to NaN
results['accuracy'] = pd.to_numeric(results['accuracy'], errors='coerce')

# Process data for each language
for language in results['language'].unique():
    print(f"\n=== {language.upper()} ===")
    
    # Create a table with subject-specific scores and overall stats
    lang_data = results[results['language'] == language].pivot(
        index='model',
        columns='subject',
        values='accuracy'
    )
    
    # Add mean and std columns
    lang_data['mean'] = lang_data.mean(axis=1).round(2)  # Calculate mean across all subjects
    lang_data['std'] = lang_data.std(axis=1).round(2)    # Calculate standard deviation across all subjects
    
    # sort by mean
    lang_data = lang_data.sort_values('mean', ascending=False)

    # Print and save results
    print("\nResults (including subject scores and overall statistics):")
    print(lang_data.round(2))
    lang_data.to_csv(os.path.join(output_dir, f'{language}_stats.csv'))
