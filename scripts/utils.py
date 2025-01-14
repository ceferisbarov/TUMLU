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
    "crimean-tatar": """Sual: {question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n\nCevap: {answer}\n\n""",
    "uzbek": """Savol: {question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n\nJavob: {answer}\n\n""",
    "tatar": """Сорау: {question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n\nҖавап: {answer}\n\n""",
}
TEST_PROMPTS = {
    "crimean-tatar": """Sual: {question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n\nCevap: """,
    "uzbek": """Savol: {question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n\nJavob: """,
    "tatar": """Сорау: {question}\nA) {choices[0]}\nB) {choices[1]}\nC) {choices[2]}\nD) {choices[3]}\n\nҖавап: """,
}

CRIMEAN_FEW_SHOT_TEMPLATE = """Sual: {question}\n{choices}\n\nCevap: {answer}\n\n"""
CRIMEAN_TEST_TEMPLATE = """Sual: {question}\n{choices}\n\nCevap: \n\n"""


def format_question(template, question, choices, answer=None):
    # Dynamically generate the choices section
    choices_text = "\n".join(
        f"{chr(65 + i)}) {choice}" for i, choice in enumerate(choices)
    )
    if answer:
        return CRIMEAN_FEW_SHOT_TEMPLATE.format(
            question=question, choices=choices_text, answer=answer
        )

    return CRIMEAN_TEST_TEMPLATE.format(question=question, choices=choices_text)


if __name__ == "__main__":
    question = "What is the capital of France?"
    choices = ["Paris", "London", "Berlin", "Madrid"]  # This can have 2-4 items
    answer = "Paris"

    formatted_question = format_question(
        CRIMEAN_FEW_SHOT_TEMPLATE, question, choices, answer
    )
    print(formatted_question)

    print(format_question(CRIMEAN_TEST_TEMPLATE, question, choices))
