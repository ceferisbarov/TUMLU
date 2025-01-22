# TurkicMMLU: A Unified and Native Language Understanding Benchmark for Turkic Languages

This repo contains the code and data necessary to replicate results of TurkicMMLU paper. Dataset is hosted on [Hugging Face](https://huggingface.co/datasets/allmalab/TurkicMMLU) by aLLMA Lab. **Please, don't submit access requeset with a temporary email.** We approve requests within a day. If delayed, feel free to remind us via email. 

## Dataset
TurkicMMLU spans 8 Turkic languages, with plans to add more.
- [x] Azerbaijani
- [x] Crimean Tatar
- [x] Karakalpak
- [x] Kazakh
- [x] Tatar
- [x] Turkish
- [x] Uyghur
- [x] Uzbek
- [ ] Kyrgyz

All questions are at middle- and high-school level. All questions are native, i.e., not translated or synthetically generated. There can be some difference in difficuly levels across languages.
## How to use
Set up the environment:
```sh
uv venv env

source env/bin/activate

uv pip install -r requirements.txt

touch .env
```

Add the following api keys to the `.env` file:
```
OPENAI_API_KEY=""
ANTHROPIC_API_KEY=""
TOGETHER_API_KEY=""
GEMINI_API_KEY=""
DEEPINFRA_API_KEY=""
```

Run `scripts/fewshot.py` from the base folder to run 5-shot benchmarks. You need to specify models and languages from within the script. If anybody wants to create friendly CLI with Fire, PRs are welcome!

All results are stored in `data` directory. `scripts/evaluate.py` can be used to print accuracy of a single language-model combination. `scripts/aggregate.py` creates a CSV file containing all language-model-subject combinations.

## Contributions
All issues and PRs are welcome! We are particularly grateful for any feedback on data quality, even if it is a simple typo that we have missed.
  
Our team consists of the following people, in alphabetical order:

- Abdullatif Köksal
- Anar Rzayev
- Arofat Akhundjanova
- Dmitry Gaynullin
- Duyghu Ataman
- Jafar Isbarov
- Kavsar Huseynova
- Mammad Hajili
- Osman Tursun
- Samir Rustamov
- Saule Belginova

## Citation
If you use this dataset or code in your work, please, cite us:
```bib
{
    placeholder
}
```
