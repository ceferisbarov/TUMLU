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
    "claude-3-5-sonnet-20241022",
    "claude-3-5-haiku-20241022",
    "gpt-4o-2024-11-20",
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Llama-3.3-70B-Instruct",
    "gemini-1.5-flash",
    # "gemini-2.0-flash-exp", # very low rate limits, ignore
    "gemini-1.5-pro",
    "google/gemma-2-27b-it",
    "google/gemma-2-9b-it",
]

FEW_SHOT_PROMPTS = {
    "crimean-tatar": """Sual: {question}\n{choices}\n\nCevap: {answer}\n\n""",
    "uzbek": """Savol: {question}\n{choices}\n\nJavob: {answer}\n\n""",
    "tatar": """Сорау: {question}\n{choices}\n\nҖавап: {answer}\n\n""",
    "kazakh": """Сұрақ: {question}\n{choices}\n\nЖауап: {answer}\n\n""",
    "karakalpak": """Soraw: {question}\n{choices}\n\nJuwap: {answer}\n\n""",
    "turkish": """Soru: {question}\n{choices}\n\nCevap: {answer}\n\n""",
    "uyghur": """سوئال: {question}\n{choices}\n\nجاۋاب: {answer}\n\n""",
    "azerbaijani": """Sual: {question}\n{choices}\n\nCavab: {answer}\n\n""",
}

TEST_PROMPTS = {
    "crimean-tatar": """Sual: {question}\n{choices}\n\nCevap: """,
    "uzbek": """Savol: {question}\n{choices}\n\nJavob: """,
    "tatar": """Сорау: {question}\n{choices}\n\nҖавап: """,
    "kazakh": """Сұрақ: {question}\n{choices}\n\nЖауап: """,
    "karakalpak": """Soraw: {question}\n{choices}\n\nJuwap: """,
    "turkish": """Soru: {question}\n{choices}\n\nCevap: """,
    "uyghur": """سوئال: {question}\n{choices}\n\nجاۋاب: """,
    "azerbaijani": """Sual: {question}\n{choices}\n\nCavab: """,
}

ANSWER_DICT = {
    "uzbek": "Javob",
    "crimean-tatar": "Cevap",
    "tatar": "Җавап",
    "kazakh": "Жауап",
    "karakalpak": "Juwap",
    "turkish": "Cevap",
    "uyghur": "جاۋاب",
    "azerbaijani": "Cavab",
}

QUESTION_DICT = {
    "uzbek": "Javob",
    "crimean-tatar": "Cevap",
    "tatar": "Җавап",
    "kazakh": "Жауап",
    "karakalpak": "Juwap",
    "turkish": "Cevap",
    "uyghur": "جاۋاب",
    "azerbaijani": "Sual",
}

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
    text = text.replace("А", "A")
    text = text.replace("Б", "B")
    text = text.replace("С", "C")
    text = text.replace("Д", "D")

    word = ANSWER_DICT[language]
    patterns = {
        "A": [r"A\)", rf"{word}: A", rf"{word} A\)", r"\*\*A\*\*"],
        "B": [r"B\)", rf"{word}: B", rf"{word} B\)", r"\*\*B\*\*"],
        "C": [r"C\)", rf"{word}: C", rf"{word} C\)", r"\*\*C\*\*"],
        "D": [r"D\)", rf"{word}: D", rf"{word} D\)", r"\*\*D\*\*"],
    }

    for letter, letter_patterns in patterns.items():
        for pattern in letter_patterns:
            if re.search(pattern, text):
                return letter

    return None


def get_acc(data, language):
    """
    Calculates accuracy of an LLM on a given dataset.
    """
    for i in data:
        i["prediction"] = find_matching_pattern(i["output"], language)

    if len(data):
        return sum(map(lambda x: x["prediction"] == x["answer"], data)) / len(data)

    return 0
