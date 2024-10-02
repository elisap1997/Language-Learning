# Creating a self-assessed ILR level quiz based on the user's ability to perform tasks in a foreign language.
# The questions will cover various skills and situations, and the user will be scored based on their answers.

# Define the questions and corresponding scores for the quiz
def ilr_quiz():
    print("Welcome to the ILR Language Proficiency Self-Assessment Quiz!")
    print("Answer the following questions to estimate your ILR level.")
    print("For each question, please enter a number between 1 (Strongly Disagree) and 5 (Strongly Agree).\n")

    # Questions mapping to the ILR levels
    questions = [
        "I can understand basic words and phrases in the language.",
        "I can carry out simple conversations in routine settings, like asking for directions or ordering food.",
        "I can engage in more complex conversations about common topics (e.g., work, family, hobbies).",
        "I can understand conversations on a wide range of topics, including abstract ideas.",
        "I can understand and use idiomatic expressions and complex grammar structures in professional situations.",
        "I can discuss specialized topics (e.g., politics, economics, technology) with near-native fluency.",
        "I can understand the language fully, including slang, idioms, and cultural references."
    ]

    # Scores will range from 1 to 5 for each question.
    score = 0
    for i, question in enumerate(questions):
        while True:
            try:
                response = int(input(f"Q{i+1}: {question} (1-5): "))
                if 1 <= response <= 5:
                    score += response
                    break
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    # Maximum possible score is 35 (7 questions * 5 max points).
    # Map scores to ILR levels based on approximate ranges.
    if score <= 7:
        ilr_level = "Level 0 – No Proficiency"
    elif score <= 14:
        ilr_level = "Level 1 – Elementary Proficiency"
    elif score <= 21:
        ilr_level = "Level 2 – Limited Working Proficiency"
    elif score <= 28:
        ilr_level = "Level 3 – Professional Working Proficiency"
    elif score <= 34:
        ilr_level = "Level 4 – Full Professional Proficiency"
    else:
        ilr_level = "Level 5 – Native or Bilingual Proficiency"

    print(f"\nBased on your answers, your estimated ILR level is: {ilr_level}")

# Run the quiz
ilr_quiz()
