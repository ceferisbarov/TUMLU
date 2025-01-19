import random


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


FEW_SHOT_PROMPTS = {
    "crimean-tatar": """Sual: {question}\n{choices}\n\nCevap: {answer}\n\n""",
    "uzbek": """Savol: {question}\n{choices}\n\nJavob: {answer}\n\n""",
    "tatar": """Сорау: {question}\n{choices}\n\nҖавап: {answer}\n\n""",
    "kazakh": """Сұрақ: {question}\n{choices}\n\nЖауап: {answer}\n\n""",
}

TEST_PROMPTS = {
    "crimean-tatar": """Sual: {question}\n{choices}\n\nCevap: """,
    "uzbek": """Savol: {question}\n{choices}\n\nJavob: """,
    "tatar": """Сорау: {question}\n{choices}\n\nҖавап: """,
    "kazakh": """Сұрақ: {question}\n{choices}\n\nЖауап: """,
}


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
