# TUMLU: A Unified and Native Language Understanding Benchmark for Turkic Languages

This repo contains the code and data necessary to replicate results of [TUMLU paper](https://arxiv.org/abs/2502.11020). TUMLU-mini dataset is located in `data/<LANGUAGE>/test` folders. All experimental results are stored in `data/<LANGUAGE>/outputs` folders. You can analyze those without rerunning the same experiments. TUMLU-mini is also available on [Hugging Face](https://huggingface.co/datasets/jafarisbarov/TUMLU-mini).

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

## Results
### 5-shot results
| Model             | Mean | aze  | crh  | kaa  | kaz  | tat  | tur  | uig  | uzb  |
|-------------------|------|------|------|------|------|------|------|------|------|
| Claude 3.5 Sonnet | 79.3 | 84.4 | 81.2 | 75.3 | 83.0 | 84.0 | 85.7 | 71.3 | 69.1 |
| GPT-4o            | 75.1 | 82.4 | 70.5 | 70.8 | 81.0 | 80.5 | 83.7 | 66.5 | 65.4 |
| Gemini 1.5 Pro    | 74.0 | 78.6 | 70.3 | 68.2 | 78.4 | 80.5 | 80.0 | 71.0 | 65.1 |
| Gemini 1.5 Flash  | 65.6 | 72.4 | 68.0 | 61.2 | 68.6 | 68.3 | 76.6 | 57.8 | 52.1 |
| Claude 3.5 Haiku  | 63.9 | 70.6 | 62.9 | 55.2 | 69.9 | 67.5 | 78.0 | 56.6 | 50.3 |
| Llama- 3.1 405B   | 62.9 | 65.9 | 69.5 | 60.0 | 69.0 | 70.4 | 59.7 | 58.2 | 50.4 |
| Qwen2.5 72B       | 61.5 | 70.1 | 61.8 | 54.6 | 62.6 | 62.5 | 73.9 | 56.0 | 50.4 |
| Llama 3.3 70B     | 58.4 | 66.0 | 58.7 | 49.2 | 60.0 | 69.5 | 68.4 | 51.6 | 44.1 |
| Llama 3.1 70B     | 57.6 | 68.1 | 57.3 | 49.9 | 56.4 | 66.2 | 64.9 | 52.4 | 45.3 |
| Gemma 2 27b       | 51.6 | 58.1 | 49.8 | 47.6 | 58.4 | 54.9 | 64.3 | 42.2 | 37.6 |
| Gemma 2 9b        | 46.8 | 53.7 | 46.8 | 40.8 | 49.1 | 51.8 | 60.4 | 35.8 | 36.1 |
| Qwen2.5 7B        | 42.1 | 48.0 | 42.6 | 37.2 | 45.0 | 40.5 | 55.6 | 33.4 | 34.6 |
| Llama 3.1 8B      | 40.1 | 48.4 | 35.7 | 33.4 | 46.4 | 44.1 | 47.7 | 35.0 | 29.9 |

### 5-shot chain-of-thought results
| Model | Mean | aze | kaz | tur | uzb |
|-------|------|-----|-----|-----|-----|
| Claude 3.5 Sonnet | 83.0 | **87.1 (+2.7)** | **84.1 (+1.1)** | **87.9 (+2.1)** | **72.9 (+3.7)** |
| GPT-4o | 78.5 | 82.9 (+0.4) | 80.7 (-0.3) | 84.0 (+0.3) | 66.3 (+0.9) |
| Gemini 1.5 Pro | 75.8 | 80.0 (+1.4) | 75.1 (-3.3) | 81.0 (+1.0) | 67.0 (+1.9) |
| Llama 3.1 405B | 69.8 | 73.4 (+7.6) | 68.7 (-0.3) | 80.7 (+21.0) | 56.4 (+6.0) |
| Claude 3.5 Haiku | 69.4 | 77.0 (+6.4) | 74.0 (+4.1) | 77.6 (-0.4) | 49.0 (-1.3) |
| Gemini 1.5 Flash | 67.6 | 73.9 (+1.4) | 69.0 (+0.4) | 73.6 (-3.0) | 54.1 (+2.0) |
| Qwen2.5 72B | 67.0 | 72.1 (+2.0) | 63.9 (+1.3) | 78.4 (+4.6) | 53.6 (+3.1) |
| Llama 3.3 70B | 66.9 | 70.6 (+4.6) | 69.3 (+9.3) | 77.4 (+9.0) | 50.4 (+6.3) |
| Gemma 2 27B | 59.0 | 63.0 (+4.9) | 61.6 (+3.1) | 66.4 (+2.1) | 44.9 (+7.3) |
| Llama 3.1 70B | 55.6 | 59.4 (-8.7) | 61.7 (+5.3) | 73.3 (+8.4) | 27.9 (-17.4) |
| Gemma 2 9B | 52.4 | 57.3 (+3.6) | 52.7 (+3.6) | 62.3 (+1.9) | 37.4 (+1.3) |
| Qwen2.5 7B | 47.2 | 48.1 (+0.1) | 46.4 (+1.4) | 56.3 (+0.7) | 38.0 (+3.4) |
| Llama 3.1 8B | 37.8 | 40.7 (-7.7) | 38.9 (-7.6) | 45.1 (-2.6) | 26.6 (-3.3) |

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
DEEPSEEK_API_KEY="" # if you also want to test deepseek models
```

Run `scripts/fewshot.py` from the base folder to run 5-shot benchmarks. You need to specify models and languages from within the script. If anybody wants to create friendly CLI with Fire, PRs are welcome!

All results are stored in `data` directory. `scripts/evaluate.py` can be used to print accuracy of a single language-model combination. `scripts/aggregate.py` creates CSV files and LaTeX tables containing all language-model-subject combinations.

## Contributions
All issues and PRs are welcome! We are particularly grateful for any feedback on data quality, even if it is a simple typo that we have missed.
  
Our team consists of the following people, in alphabetical order:

- Abdullatif Köksal
- Amina Alisheva
- Anar Rzayev
- Ariana Kenbayeva
- Arofat Akhundjanova
- Aizirek Turdubaeva
- Dmitry Gaynullin
- Duygu Ataman
- Ilshat Saetov
- Jafar Isbarov
- Kavsar Huseynova
- Mammad Hajili
- Osman Tursun
- Rinat Kharisov
- Samir Rustamov
- Saule Belginova

## Citation
If you use this dataset or code in your work, please, cite us:
```bib
@misc{isbarov2025tumluunifiednativelanguage,
    title={{TUMLU: A Unified and Native Language Understanding Benchmark for Turkic Languages}}, 
    author={Jafar Isbarov and Arofat Akhundjanova and Mammad Hajili and Kavsar Huseynova and Dmitry Gaynullin and Anar Rzayev and Osman Tursun and Ilshat Saetov and Rinat Kharisov and Saule Belginova and Ariana Kenbayeva and Amina Alisheva and Aizirek Turdubaeva and Abdullatif Köksal and Samir Rustamov and Duygu Ataman},
    year={2025},
    eprint={2502.11020},
    archivePrefix={arXiv},
    primaryClass={cs.CL},
    url={https://arxiv.org/abs/2502.11020}, 
}
```
