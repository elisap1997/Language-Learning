class ILRQuiz:
    def __init__(self):
        self.categories = ["Reading", "Writing", "Speaking", "Listening"]
        self.questions = {
            "Reading": [
                {"text": "I can understand basic written words and phrases.", "weight": 1},
                {"text": "I can comprehend simple texts on familiar topics.", "weight": 2},
                {"text": "I can understand complex texts on a wide range of topics.", "weight": 3},
                {"text": "I can interpret sophisticated literary texts.", "weight": 4}
            ],
            "Writing": [
                {"text": "I can write basic phrases and simple sentences.", "weight": 1},
                {"text": "I can write short texts on familiar topics.", "weight": 2},
                {"text": "I can write detailed texts on a wide range of subjects.", "weight": 3},
                {"text": "I can write complex texts in appropriate styles.", "weight": 4}
            ],
            "Speaking": [
                {"text": "I can use basic phrases and sentences.", "weight": 1},
                {"text": "I can participate in simple conversations on familiar topics.", "weight": 2},
                {"text": "I can express myself fluently on a wide range of subjects.", "weight": 3},
                {"text": "I can use the language flexibly for social, academic, and professional purposes.", "weight": 4}
            ],
            "Listening": [
                {"text": "I can understand basic spoken phrases.", "weight": 1},
                {"text": "I can understand the main points of clear speech on familiar matters.", "weight": 2},
                {"text": "I can understand extended speech and complex arguments.", "weight": 3},
                {"text": "I can understand any kind of spoken language with ease.", "weight": 4}
            ]
        }
        self.levels = [
            {"max_score": 5, "name": "Level 0 – No Proficiency"},
            {"max_score": 10, "name": "Level 1 – Elementary Proficiency"},
            {"max_score": 15, "name": "Level 2 – Limited Working Proficiency"},
            {"max_score": 20, "name": "Level 3 – Professional Working Proficiency"},
            {"max_score": 25, "name": "Level 4 – Full Professional Proficiency"},
            {"max_score": float('inf'), "name": "Level 5 – Native or Bilingual Proficiency"}
        ]

    def run_quiz(self):
        print("Welcome to the ILR Language Proficiency Self-Assessment Quiz!")
        print("This quiz will assess your skills in Reading, Writing, Speaking, and Listening.")
        print("For each question, please enter a number between 1 (Strongly Disagree) and 5 (Strongly Agree).\n")

        scores = {category: 0 for category in self.categories}

        for category in self.categories:
            print(f"\n{category.upper()} ASSESSMENT")
            for i, question in enumerate(self.questions[category]):
                while True:
                    try:
                        response = int(input(f"Q{i+1}: {question['text']} (1-5): "))
                        if 1 <= response <= 5:
                            scores[category] += response * question['weight']
                            break
                        else:
                            print("Please enter a number between 1 and 5.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

        print("\nYour ILR Proficiency Levels:")
        for category, score in scores.items():
            ilr_level = next(level['name'] for level in self.levels if score <= level['max_score'])
            print(f"{category}: {ilr_level} (Score: {score:.2f})")

        overall_score = sum(scores.values()) / len(scores)
        overall_level = next(level['name'] for level in self.levels if overall_score <= level['max_score'])
        print(f"\nOverall ILR Level: {overall_level} (Average Score: {overall_score:.2f})")

if __name__ == "__main__":
    quiz = ILRQuiz()
    quiz.run_quiz()
