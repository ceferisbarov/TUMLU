import os
import json
from itertools import product
import pandas as pd
from typing import Dict, List, Optional
from pathlib import Path

from utils import LANGUAGES, MODEL_NAMES, get_acc

def load_and_process_data(
    base_dir: str,
    languages: list[str],
    model_names: list[str],
    get_acc_fn
) -> pd.DataFrame:
    """
    Load and process model evaluation data from the specified directory structure.
    
    Args:
        base_dir: Root directory containing the data
        languages: List of language codes to process
        model_names: List of model names to evaluate
        get_acc_fn: Function to calculate accuracy from raw data
        
    Returns:
        DataFrame containing processed results
    """
    results = []
    
    for language, model in product(languages, model_names):
        base_path = Path(base_dir) / language / "outputs/no_cot_instruct" / model
        
        if not base_path.exists():
            continue
            
        for subject_file in base_path.iterdir():
            subject = subject_file.name.lower().replace('.json', '')  # This is line we changed

            try:
                if not subject_file.is_file():
                    results.append({
                        "language": language,
                        "model": model,
                        "subject": subject,
                        "accuracy": None
                    })
                    continue
                    
                data = json.loads(subject_file.read_text(encoding="utf-8"))
                accuracy = 100 * round(get_acc_fn(data, language), 4)
                
                results.append({
                    "language": language,
                    "model": model,
                    "subject": subject,
                    "accuracy": accuracy
                })
                
            except Exception as e:
                print(f"Error processing {subject_file}: {str(e)}")
                continue
    
    return pd.DataFrame(results)

def generate_language_statistics(
    results: pd.DataFrame,
    output_dir: str
) -> dict[str, pd.DataFrame]:
    """
    Generate and save statistics for each language.
    
    Args:
        results: DataFrame containing the processed results
        output_dir: Directory to save the output statistics
        
    Returns:
        Dictionary mapping language codes to their statistics DataFrames
    """
    Path(output_dir).mkdir(exist_ok=True)
    language_stats = {}
    
    for language in results['language'].unique():
        # print(f"\n=== {language.upper()} ===")
        
        # Create pivot table with subject-specific scores
        lang_data = results[results['language'] == language].pivot(
            index='model',
            columns='subject',
            values='accuracy'
        )
        
        # Add summary statistics
        lang_data['mean'] = lang_data.mean(axis=1).round(2)
        lang_data['std'] = lang_data.std(axis=1).round(2)
        
        # Sort by mean score
        lang_data = lang_data.sort_values('mean', ascending=False)
        
        # Print and save results
        # print("\nResults (including subject scores and overall statistics):")
        # print(lang_data.round(2))
        
        output_path = Path(output_dir) / f'{language}_stats.csv'
        lang_data.to_csv(output_path)
        print(f"Saved statistics for {language} at {output_path}")
        
        language_stats[language] = lang_data
        
    return language_stats


def generate_model_tables(
    results: pd.DataFrame,
    output_dir: str
) -> None:
    """
    Generate CSV tables for each model showing performance across languages and subjects.
    
    Args:
        results: DataFrame containing the processed results
        output_dir: Directory to save the CSV tables
    """
    tables_dir = Path(output_dir)
    tables_dir.mkdir(exist_ok=True)
    
    # Get unique subjects and sort them
    subjects = sorted(results['subject'].unique())
    
    for model in results['model'].unique():
        # Create pivot table for this model
        model_data = results[results['model'] == model].pivot(
            index='language',
            columns='subject',
            values='accuracy'
        )
        
        # Round values
        model_data = model_data.round(2)
        
        # Calculate mean for each language
        model_data['mean'] = model_data.mean(axis=1).round(2)
        
        # Calculate mean for each subject
        means = model_data.mean().round(2)
        model_data.loc['mean'] = means
        
        # Save to CSV
        model_filename = model.lower().replace('/', '_')
        output_path = tables_dir / f"{model_filename}_table.csv"
        model_data.to_csv(output_path)
        print(f"Generated table for {model} at {output_path}")

def clean(results):

    subject_dict = {
        "Logic": ["logic"],
        "Maths": ["math", "maths", "mathematics"],
        "Physics": ["phsyics", "physics"],
        "Chemistry": ["chemistry"],
        "Biology": ["biology"],
        "Geography": ["geography"],
        "History": ["history of russia", "history", "history-of-kazakhstan"],
        "Native L&L": ["turkish_language_and_literature", "uyghur_literature&grammar", "kazakh", "language", "language & literature", "language and literature"],
        "Human and Society": ["human & society"],
        "Philosophy": ["philosophy"],
        "Religion and Ethics": ["religion_and_ethics"]
    }

    subjects_to_skip = ["computer science", "world-history", "Logic", "Religion and Ethics", "Human and Society", "Philosophy"]

    # Replacing subject names
    results["subject"] = results["subject"].replace({v: k for k, values in subject_dict.items() for v in values})

    # Dropping rows with subjects in subjects_to_skip
    results = results[~results["subject"].isin(subjects_to_skip)]

    return results

def generate_latex_per_language(results, output_dir) -> None:
    """
    Generate LaTeX tables for each language showing accuracy scores per subject.

    Args:
        results (pd.DataFrame): DataFrame containing processed results.
        output_dir (str): Directory to save LaTeX tables.
    """

    results = clean(results)

    tables_dir = Path(output_dir)
    tables_dir.mkdir(parents=True, exist_ok=True)

    for language in results['language'].unique():
        lang_data = results[results['language'] == language].pivot(
            index='model',
            columns='subject',
            values='accuracy'
        )

        lang_data = lang_data.sort_index(axis=1)  # Sort subjects (columns) alphabetically
        lang_data = lang_data.sort_index(axis=0)  # Sort models (index) alphabetically
        lang_data.fillna('-', inplace=True) # fill none values wit '-'

        latex_template = """\\begin{table*}
\\centering
\\begin{tabular}{l<cols>}
\\hline
\\textbf{Model} & <subjects>\\\\
\\hline
<data> \\\\
\\hline
\\end{tabular}
\\caption{<caption>}
\\label{tab:<tag>}
\\end{table*}"""

        # declaring centered cols
        num_columns = len(lang_data.columns)
        cols = 'c'*num_columns
        latex_template = latex_template.replace("<cols>", cols)

        # putting subject names as header
        column_names = lang_data.columns.tolist()
        column_names = ['\\textbf{'+i+'}' for i in column_names]
        subjects = ' & '.join(column_names)
        latex_template = latex_template.replace("<subjects>", subjects)

        # put data in its place
        rows = lang_data.values.tolist()
        model_names = lang_data.index.tolist()
        for i in range(len(rows)):
            row = rows[i]
            model = model_names[i]
            row = [model.capitalize()] + [f'{acc:.2f}' if not isinstance(acc, str) else acc for acc in row]
            row = ' & '.join(row)
            rows[i] = row
        data = ' \\\\\n'.join(rows)
        latex_template = latex_template.replace("<data>", data)

        # putting the caption
        caption=f"Accuracy scores for {language.upper()} models across subjects."
        latex_template = latex_template.replace("<caption>", caption)

        # putting the tag
        tag = f"{language}_accuracy"
        latex_template = latex_template.replace("<tag>", tag)

        # Save to file
        output_path = tables_dir / f"{language}.tex"
        with open(output_path, "w") as f:
            f.write(latex_template)

        print(f"Generated LaTeX table for {language} at {output_path}")

def generate_latex_per_model(results, output_dir) -> None:
    """
    Generate LaTeX tables for each language showing accuracy scores per subject.

    Args:
        results (pd.DataFrame): DataFrame containing processed results.
        output_dir (str): Directory to save LaTeX tables.
    """

    results = clean(results)

    tables_dir = Path(output_dir)
    tables_dir.mkdir(parents=True, exist_ok=True)

    for model in results['model'].unique():
        # Create pivot table for this model
        model_data = results[results['model'] == model].pivot(
            index='language',
            columns='subject',
            values='accuracy'
        )

        model_data = model_data.sort_index(axis=1)  # Sort subjects (columns) alphabetically
        model_data = model_data.sort_index(axis=0)  # Sort languages (index) alphabetically
        model_data.fillna('-', inplace=True) # fill none values wit '-'

        latex_template = """\\begin{table*}
\\centering
\\begin{tabular}{l<cols>}
\\hline
\\textbf{Languages} & <subjects>\\\\
\\hline
<data> \\\\
\\hline
\\end{tabular}
\\caption{<caption>}
\\label{tab:<tag>}
\\end{table*}"""

        # declaring centered cols
        num_columns = len(model_data.columns)
        cols = 'c'*num_columns
        latex_template = latex_template.replace("<cols>", cols)

        # putting subject names as header
        column_names = model_data.columns.tolist()
        column_names = ['\\textbf{'+i+'}' for i in column_names]
        subjects = ' & '.join(column_names)
        latex_template = latex_template.replace("<subjects>", subjects)

        # put data in its place
        rows = model_data.values.tolist()
        lang_names = model_data.index.tolist()
        for i in range(len(rows)):
            row = rows[i]
            lang = lang_names[i]
            row = [lang.capitalize()] + [f'{acc:.2f}' if not isinstance(acc, str) else acc for acc in row]
            row = ' & '.join(row)
            rows[i] = row
        data = ' \\\\\n'.join(rows)
        latex_template = latex_template.replace("<data>", data)

        # putting the caption
        caption=f"Accuracy scores for {model.upper()} model across languages."
        latex_template = latex_template.replace("<caption>", caption)

        # putting the tag
        tag = f"{model}_accuracy"
        latex_template = latex_template.replace("<tag>", tag)

        # Save to file
        model_filename = model.lower().replace('/', '_')
        output_path = tables_dir / f"{model_filename}.tex"
        with open(output_path, "w") as f:
            f.write(latex_template)

        print(f"Generated LaTeX table for {model} at {output_path}")

def main():
    # Configuration
    base_dir = "data"
    output_dir = "results"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load results
    results = load_and_process_data(
        base_dir=base_dir,
        languages=LANGUAGES,
        model_names=MODEL_NAMES,
        get_acc_fn=get_acc
    )
    
    # Save overall results
    results.to_csv(Path(output_dir) / "results.csv", index=False)
    
    # Convert accuracy to numeric, handling errors
    results['accuracy'] = pd.to_numeric(results['accuracy'], errors='coerce')
    
    # Generate per-language statistics
    language_stats = generate_language_statistics(results, output_dir + "/language_stats")
    
    # Generate model tables in csv
    generate_model_tables(results, output_dir + "/model_stats")

    # Generate LaTeX tables
    language_tables_path = os.path.join(output_dir, "tables", "language")
    generate_latex_per_language(results, language_tables_path)

    model_tables_path = os.path.join(output_dir, "tables", "model")
    generate_latex_per_model(results, model_tables_path)

    return results, language_stats

if __name__ == "__main__":
    main()
