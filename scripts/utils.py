import re
import random

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
    # "claude-3-5-sonnet-v2@20241022", # testing claude@Vertex AI vs claude@Anthropic
    # "claude-3-5-haiku@20241022", # testing claude@Vertex AI vs claude@Anthropic
    "gpt-4o-2024-11-20",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
    "gemini-1.5-flash",
    # "gemini-2.0-flash-exp", # very low rate limits, ignore
    "gemini-1.5-pro",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    # "deepseek-chat",
]

FEW_SHOT_PROMPTS = {
    "crimean-tatar": """Sual: {question}\n{choices}\n\nCevap: {answer}\n\n""",
    "crimean-tatar-cyrillic": """Суаль: {question}\n{choices}\n\nДжевап: {answer}\n\n""",
    "uzbek": """Savol: {question}\n{choices}\n\nJavob: {answer}\n\n""",
    "uzbek-cyrillic": """Савол: {question}\n{choices}\n\nЖавоб: {answer}\n\n """,
    "tatar": """Сорау: {question}\n{choices}\n\nҖавап: {answer}\n\n""",
    "kazakh": """Сұрақ: {question}\n{choices}\n\nЖауап: {answer}\n\n""",
    "kazakh-latin": """Suraq: {question}\n{choices}\n\nJawap: {answer}\n\n""",
    "karakalpak": """Soraw: {question}\n{choices}\n\nJuwap: {answer}\n\n""",
    "turkish": """Soru: {question}\n{choices}\n\nCevap: {answer}\n\n""",
    "uyghur": """سوئال: {question}\n{choices}\n\nجاۋاب: {answer}\n\n""",
    "azerbaijani": """Sual: {question}\n{choices}\n\nCavab: {answer}\n\n""",
}

TEST_PROMPTS = {
    "crimean-tatar": """Sual: {question}\n{choices}\n\nCevap: """,
    "crimean-tatar-cyrillic": """Суаль: {question}\n{choices}\n\nДжевап: """,
    "uzbek": """Savol: {question}\n{choices}\n\nJavob: """,
    "uzbek-cyrillic": """Савол: {question}\n{choices}\n\nЖавоб: """,
    "tatar": """Сорау: {question}\n{choices}\n\nҖавап: """,
    "kazakh": """Сұрақ: {question}\n{choices}\n\nЖауап: """,
    "kazakh-latin": """Suraq: {question}\n{choices}\n\nJawap: """,
    "karakalpak": """Soraw: {question}\n{choices}\n\nJuwap: """,
    "turkish": """Soru: {question}\n{choices}\n\nCevap: """,
    "uyghur": """سوئال: {question}\n{choices}\n\nجاۋاب: """,
    "azerbaijani": """Sual: {question}\n{choices}\n\nCavab: """,
}

ANSWER_DICT = {
    "uzbek": "Javob",
    "uzbek-cyrillic": "Жавоб",
    "crimean-tatar": "Cevap",
    "crimean-tatar-cyrillic": "Джевап",
    "tatar": "Җавап",
    "kazakh": "Жауап",
    "kazakh-latin": "Jawap",
    "karakalpak": "Juwap",
    "turkish": "Cevap",
    "uyghur": "جاۋاب",
    "azerbaijani": "Cavab",
}

QUESTION_DICT = {
    "uzbek": "Savol",
    "uzbek-cyrillic": "Савол",
    "crimean-tatar": "Sual",
    "tatar": "Сорау",
    "kazakh": "Сұрақ",
    "kazakh-latin": "Suraq",
    "karakalpak": "Soraw",
    "turkish": "Soru",
    "uyghur": "سوئال",
    "azerbaijani": "Sual",
}

SOLUTION_DICT = {
    "uzbek": "yechim",
    "uzbek-cyrillic": "ечим",
    "crimean-tatar": "irinti",
    "tatar": "чишелеш",
    "kazakh": "шешім",
    "kazakh-latin": "şeşim",
    "turkish": "çözüm",
    "uyghur": "ھهل",
    "azerbaijani": "həll",
}


def format_fewshot_prompt(language, question, choices, answer=None):
    template = "{question_keyword.title()}: {question}\n{choices}\n{answer_keyword.title()}: {answer}"
    template_no_answer = (
        "{question_keyword.title()}: {question}\n{choices}\n{answer_keyword.title()}: "
    )
    choices_text = "\n".join(
        f"{chr(65 + i)}) {choice}" for i, choice in enumerate(choices)
    )
    question_keyword = QUESTION_DICT[language]
    answer_keyword = ANSWER_DICT[language]
    if answer:
        return template.format(
            question_keyword=question_keyword,
            question=question,
            choices=choices_text,
            answer_keyword=answer_keyword.title(),
            answer=answer,
        )

    return template_no_answer.format(
        question_keyword=question_keyword,
        question=question,
        choices=choices_text,
        answer_keyword=answer_keyword.title(),
    )


def format_CoT_prompt(language, question, choices, solution=None):
    """
    Given a language specific template, question, choices,
    format and return the template.
    answer argument is necessary for FEW_SHOT_PROMPTS but not for TEST_PROMPTS.
    """
    template = (
        "{question_keyword}: {question}\n{choices}\n{solution_keyword}: {solution}"
    )
    template_no_solution = (
        "{question_keyword}: {question}\n{choices}\n{solution_keyword}: "
    )
    choices_text = "\n".join(
        f"{chr(65 + i)}) {choice}" for i, choice in enumerate(choices)
    )
    question_keyword = QUESTION_DICT[language]
    solution_keyword = SOLUTION_DICT[language]
    if solution:
        return template.format(
            question_keyword=question_keyword.title(),
            question=question,
            choices=choices_text,
            solution_keyword=solution_keyword.title(),
            solution=solution,
        )

    return template_no_solution.format(
        question_keyword=question_keyword.title(),
        question=question,
        choices=choices_text,
        solution_keyword=solution_keyword.title(),
    )


def shuffle_choices(options, answer):
    """
    Shuffles the given list of options and updates the corresponding answer.

    Args:
      options: A list of strings representing the options for the MCQ question.
      answer: A string representing the correct answer (e.g., 'a', 'b', 'c', 'd').

    Returns:
      A tuple containing:
        - The shuffled list of options.
        - The updated answer corresponding to the shuffled options.
    """

    shuffled_options = options[:]  # Create a copy of the original list
    random.shuffle(shuffled_options)

    # Determine the index of the original answer in the shuffled list
    original_index = options.index(options[ord(answer) - ord("A")])
    shuffled_index = shuffled_options.index(options[original_index])

    # Update the answer based on the shuffled index
    updated_answer = chr(shuffled_index + ord("A"))

    return shuffled_options, updated_answer.upper()


def format_question(template, question, choices, answer=None):
    """
    Given a language specific template, question, choices,
    format and return the template.
    answer argument is necessary for FEW_SHOT_PROMPTS but not for TEST_PROMPTS.
    """
    choices_text = "\n".join(
        f"{chr(65 + i)}) {choice}" for i, choice in enumerate(choices)
    )
    if answer:
        return template.format(question=question, choices=choices_text, answer=answer)

    return template.format(question=question, choices=choices_text)


def find_matching_pattern(text, language):
    """
    Given an LLM output, matches it to A, B, C, or D.
    """
    text = re.sub(r"\s+", " ", text)
    text = text.replace("*", "")
    text = text.replace("А", "A")
    text = text.replace("В", "B")
    text = text.replace("Б", "B")
    text = text.replace("С", "C")
    text = text.replace("Д", "D")

    word = ANSWER_DICT[language]
    patterns = {
        "A": [
            rf"{word}: A",
            rf"{word.lower()}: A",
            rf"{word} A\)",
            rf"{word.lower()} A\)",
            rf"{word} A ",
            rf"{word.lower()} A ",
            r"A\)",
        ],
        "B": [
            rf"{word}: B",
            rf"{word.lower()}: B",
            rf"{word} B\)",
            rf"{word.lower()} B\)",
            rf"{word} B ",
            rf"{word.lower()} B ",
            r"B\)",
        ],
        "C": [
            rf"{word}: C",
            rf"{word.lower()}: C",
            rf"{word} C\)",
            rf"{word.lower()} C\)",
            rf"{word} C ",
            rf"{word.lower()} C ",
            r"C\)",
        ],
        "D": [
            rf"{word}: D",
            rf"{word.lower()}: D",
            rf"{word} D\)",
            rf"{word.lower()} D\)",
            rf"{word} D ",
            rf"{word.lower()} D ",
            r"D\)",
        ],
    }

    for i in range(len(patterns["A"])):
        if re.search(patterns["A"][i], text):
            return "A"
        if re.search(patterns["B"][i], text):
            return "B"
        if re.search(patterns["C"][i], text):
            return "C"
        if re.search(patterns["D"][i], text):
            return "D"

    return None


def get_acc(data, language, normalize=False):
    """
    Calculates accuracy of an LLM on a given dataset.
    """
    filtered_data = data
    for i in filtered_data:
        i["prediction"] = find_matching_pattern(i["output"], language)

    if len(data):
        if normalize:
            return sum(
                map(
                    lambda x: int(x["prediction"] == x["answer"])
                    * len(x["choices"])
                    / 4,
                    filtered_data,
                )
            ) / len(filtered_data)
        return sum(
            map(lambda x: int(x["prediction"] == x["answer"]), filtered_data)
        ) / len(filtered_data)
    return 0
