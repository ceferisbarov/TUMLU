import json
import os
from glob import glob
from pathlib import Path

from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai

from tqdm import tqdm
from dotenv import load_dotenv

from utils import shuffle_choices, FEW_SHOT_PROMPTS, TEST_PROMPTS, format_question

load_dotenv(".env")
MODEL_NAMES = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "gpt-4o-2024-11-20",
    "Qwen/Qwen2.5-7B-Instruct",
    #    "Qwen/Qwen2.5-32B-Instruct", Doesn't exist in DeepInfra
    "Qwen/Qwen2.5-72B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "gemini-1.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
]

TEMPERATURE = 0.0
MAX_TOKENS = 1024
TOP_P = 1.0
TEST_COUNT = 100
LANGUAGE = "uzbek"
SUBJECT_LIST_TEST = glob(f"data/{LANGUAGE}/test/*.jsonl")  # CHANGE LANGUAGE HERE
SUBJECT_DICT = {}
FEW_SHOT_PROMPT = FEW_SHOT_PROMPTS[LANGUAGE]
TEST_PROMPT = TEST_PROMPTS[LANGUAGE]

for MODEL_NAME in MODEL_NAMES:
    OUTPUT_PATH = f"data/{LANGUAGE}/outputs/no_cot_instruct/{MODEL_NAME}/"

    if MODEL_NAME == "gpt-4o-2024-11-20":
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    elif "claude" in MODEL_NAME:
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    elif "gemini" in MODEL_NAME:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    elif "qwen" in MODEL_NAME.lower() or "llama" in MODEL_NAME.lower():
        client = OpenAI(
            api_key=os.environ["DEEPINFRA_API_KEY"],
            base_url="https://api.deepinfra.com/v1/openai",
        )
    else:
        client = OpenAI(
            api_key=os.environ["TOGETHER_API_KEY"],
            base_url="https://api.together.xyz/v1",
        )

    for i in SUBJECT_LIST_TEST:
        SUBJECT_DICT[Path(i).stem] = {}
        SUBJECT_DICT[Path(i).stem]["path"] = i
        dev_file_path = i.replace("test", "dev")
        with open(dev_file_path, "r", encoding="utf8") as f:
            json_content = []
            for line in f:
                json_content.append(json.loads(line))

        str_content = ""
        for j in json_content:
            shuffled_choices, shuffled_answer = shuffle_choices(
                j["choices"], j["answer"]
            )

            str_content = str_content + format_question(
                FEW_SHOT_PROMPT,
                question=j["question"].strip(),
                choices=shuffled_choices,
                answer=shuffled_answer,
            )
        SUBJECT_DICT[Path(i).stem]["dev"] = str_content

    problems = {}
    for subject, content in SUBJECT_DICT.items():

        output_file = OUTPUT_PATH + subject + ".json"
        with open(content["path"], encoding="utf8") as f:
            doc = []
            for line in f:
                doc.append(json.loads(line))
        if os.path.exists(output_file):
            print(output_file, "exists...")
            continue
        problem_indexes = []
        output_dicts = []
        system = content["dev"]
        print("Subject: ", subject)
        for q in tqdm(doc[:TEST_COUNT]):
            shuffled_choices, shuffled_answer = shuffle_choices(
                q["choices"], q["answer"]
            )
            assert (
                len(shuffled_choices) <= 4
            ), "The number of choices should not be more than 4!"
            input = format_question(
                TEST_PROMPT, question=q["question"], choices=shuffled_choices
            )

            try:
                if "claude" in MODEL_NAME:
                    message = client.messages.create(
                        model=MODEL_NAME,
                        max_tokens=MAX_TOKENS,
                        temperature=TEMPERATURE,
                        system=system,
                        messages=[
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": input}],
                            },
                        ],
                    )
                    output = message.content[0].text.strip()
                elif "gemini" in MODEL_NAME:
                    client = genai.GenerativeModel(
                        MODEL_NAME, system_instruction=system
                    )
                    response = client.generate_content(
                        input,
                        generation_config=genai.GenerationConfig(
                            max_output_tokens=MAX_TOKENS,
                            temperature=TEMPERATURE,
                        ),
                    )
                    output = response.text.strip()
                else:
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[
                            {"role": "system", "content": system},
                            {"role": "user", "content": input},
                        ],
                        temperature=TEMPERATURE,
                        max_tokens=MAX_TOKENS,
                        top_p=TOP_P,
                        stop=["\n\Savol:"],
                    )
                    output = response.choices[0].message.content.strip()

            except Exception as e:
                print(e)
                problem_indexes.append(doc.index(q))
                output = "[INVALID]"

            output_dicts.append(
                {
                    "description": content["dev"],
                    "question": q["question"],
                    "choices": shuffled_choices,
                    "output": output,
                    "answer": shuffled_answer,
                    "system": system,
                    "input": input,
                }
            )
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        problems[subject] = problem_indexes
        with open(output_file, "w", encoding="utf8") as f:
            json.dump(output_dicts, f, ensure_ascii=False, indent=4)
