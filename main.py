import json
from datetime import datetime
import os

class ILRQuiz:
    def __init__(self):
        self.categories = ["Reading", "Writing", "Speaking", "Listening"]
        # Previous questions dictionary remains the same
        self.questions = {
            "Reading": [
                {"text": "I can recognize a few letters or symbols.", "weight": 1, "level": "0"},
                # ... (previous questions remain the same)
            ],
            "Writing": [
                {"text": "I can write a few letters or numbers.", "weight": 1, "level": "0"},
                # ... (previous questions remain the same)
            ],
            "Speaking": [
                {"text": "I can say a few basic words.", "weight": 1, "level": "0"},
                # ... (previous questions remain the same)
            ],
            "Listening": [
                {"text": "I can recognize a few basic words.", "weight": 1, "level": "0"},
                # ... (previous questions remain the same)
            ]
        }
        
        self.levels = [
            {"max_score": 11, "name": "Level 0 – No Proficiency"},
            {"max_score": 13, "name": "Level 0+ – Memorized Proficiency"},
            {"max_score": 16, "name": "Level 1 – Elementary Proficiency"},
            {"max_score": 18, "name": "Level 1+ – Elementary Proficiency, Plus"},
            {"max_score": 21, "name": "Level 2 – Limited Working Proficiency"},
            {"max_score": 23, "name": "Level 2+ – Limited Working Proficiency, Plus"},
            {"max_score": 26, "name": "Level 3 – Professional Working Proficiency"},
            {"max_score": 28, "name": "Level 3+ – Professional Working Proficiency, Plus"},
            {"max_score": 31, "name": "Level 4 – Full Professional Proficiency"},
            {"max_score": 33, "name": "Level 4+ – Full Professional Proficiency, Plus"},
            {"max_score": float('inf'), "name": "Level 5 – Native or Bilingual Proficiency"}
        ]
        
        self.results_file = "ilr_quiz_results.json"

    def determine_level(self, score):
        return next(level['name'] for level in self.levels if score <= level['max_score'])

    def save_results(self, user_name, language, scores, levels):
        """Save quiz results to a JSON file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            "user_name": user_name,
            "language": language,
            "date": timestamp,
            "scores": scores,
            "levels": levels
        }
        
        # Load existing results or create new list
        if os.path.exists(self.results_file):
            with open(self.results_file, 'r') as f:
                try:
                    results = json.load(f)
                except json.JSONDecodeError:
                    results = []
        else:
            results = []
        
        # Add new result
        results.append(result)
        
        # Save updated results
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=4)

    def view_results(self, user_name=None):
        """View stored quiz results, optionally filtered by username."""
        if not os.path.exists(self.results_file):
            print("No quiz results found.")
            return

        with open(self.results_file, 'r') as f:
            try:
                results = json.load(f)
            except json.JSONDecodeError:
                print("Error reading results file.")
                return

        if not results:
            print("No quiz results found.")
            return

        if user_name:
            results = [r for r in results if r["user_name"].lower() == user_name.lower()]
            if not results:
                print(f"No results found for user: {user_name}")
                return

        for result in results:
            print("\n" + "="*50)
            print(f"User: {result['user_name']}")
            print(f"Language: {result['language']}")
            print(f"Date: {result['date']}")
            print("\nCategory Scores:")
            print("-"*50)
            for category in self.categories:
                print(f"{category:10} | Score: {result['scores'][category]:6.2f} | {result['levels'][category]}")
            print("-"*50)
            print(f"Overall Level: {result['levels']['Overall']}")
            print("="*50)

    def run_quiz(self):
        print("Welcome to the ILR Language Proficiency Self-Assessment Quiz!")
        
        # Get user information
        user_name = input("Please enter your name: ")
        language = input("Which language are you assessing? ")
        
        print("\nThis quiz will assess your skills in Reading, Writing, Speaking, and Listening.")
        print("For each question, please enter a number between 1 (Strongly Disagree) and 5 (Strongly Agree).\n")

        scores = {category: 0 for category in self.categories}
        levels = {}

        for category in self.categories:
            print(f"\n{category.upper()} ASSESSMENT")
            print(f"Please answer the following questions about your {category.lower()} abilities:\n")
            
            for i, question in enumerate(self.questions[category], 1):
                while True:
                    try:
                        response = int(input(f"Q{i}: {question['text']} (1-5): "))
                        if 1 <= response <= 5:
                            scores[category] += response * question['weight']
                            break
                        else:
                            print("Please enter a number between 1 and 5.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

        # Calculate levels for each category
        print("\nYour ILR Proficiency Levels:")
        print("-" * 50)
        for category, score in scores.items():
            levels[category] = self.determine_level(score)
            print(f"{category:10} | Score: {score:6.2f} | {levels[category]}")
        print("-" * 50)

        # Calculate and display overall level
        overall_score = sum(scores.values()) / len(scores)
        overall_level = self.determine_level(overall_score)
        levels["Overall"] = overall_level
        print(f"\nOverall ILR Level: {overall_level}")
        print(f"Average Score: {overall_score:.2f}")

        # Save results
        self.save_results(user_name, language, scores, levels)
        print("\nYour results have been saved!")

def main():
    quiz = ILRQuiz()
    while True:
        print("\nILR Language Proficiency Quiz Menu:")
        print("1. Take Quiz")
        print("2. View All Results")
        print("3. View Results by Username")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            quiz.run_quiz()
        elif choice == "2":
            quiz.view_results()
        elif choice == "3":
            user_name = input("Enter username to search: ")
            quiz.view_results(user_name)
        elif choice == "4":
            print("Thank you for using the ILR Language Proficiency Quiz!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()