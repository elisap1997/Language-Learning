# quiz.py
from datetime import datetime
import os
from questions import Questions
from levels import Levels
from encryption import Encryption

class ILRQuiz:
    def __init__(self):
        self.questions = Questions.questions
        self.categories = Questions.categories
        self.results_file = "ilr_quiz_results.encrypted.json"
        self.encryption = Encryption()

    def save_results(self, user_name, language, scores, levels):
        """Save encrypted quiz results to a JSON file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            "user_name": user_name,
            "language": language,
            "date": timestamp,
            "scores": scores,
            "levels": levels
        }
        
        try:
            if os.path.exists(self.results_file):
                with open(self.results_file, 'r') as f:
                    encrypted_data = f.read()
                    results = self.encryption.decrypt_data(encrypted_data)
            else:
                results = []
            
            results.append(result)
            encrypted_results = self.encryption.encrypt_data(results)
            
            with open(self.results_file, 'w') as f:
                f.write(encrypted_results)
                
        except Exception as e:
            print(f"Error saving results: {e}")
            print("Results could not be saved. Please verify admin credentials.")

    def view_results(self, user_name=None):
        """View quiz results with admin authentication."""
        if not os.path.exists(self.results_file):
            print("No results found.")
            return

        if not self.encryption.verify_admin():
            print("Unauthorized access. Admin authentication required.")
            return

        try:
            with open(self.results_file, 'r') as f:
                encrypted_data = f.read()
                results = self.encryption.decrypt_data(encrypted_data)

            if not results:
                print("No results found.")
                return

            if user_name:
                results = [r for r in results if r["user_name"].lower() == user_name.lower()]
                if not results:
                    print(f"No results found for user: {user_name}")
                    return

            self._display_results(results)

        except Exception as e:
            print(f"Error reading results: {e}")
            print("Please verify admin credentials and try again.")

    def _display_results(self, results):
        """Helper method to display formatted results."""
        for result in results:
            print("\n" + "=" * 50)
            print(f"Name: {result['user_name']}")
            print(f"Language: {result['language']}")
            print(f"Date: {result['date']}")
            print("\nCategory Breakdown:")
            print("-" * 50)
            for category in self.categories:
                score = result['scores'][category]
                level = result['levels'][category]
                print(f"{category:10} | Score: {score:6.2f} | {level}")
            print("-" * 50)
            print(f"Overall Level: {result['levels']['Overall']}")
            print("=" * 50)

    def run_quiz(self):
        """Run the ILR proficiency quiz."""
        print("Welcome to the ILR Language Proficiency Self-Assessment Quiz!")
        
        user_name = input("Please enter your name: ").strip()
        language = input("Which language are you assessing? ").strip()
        
        self._display_instructions()
        scores, levels = self._conduct_assessment()
        
        overall_score = sum(scores.values()) / len(scores)
        overall_level = Levels.determine_level(overall_score)
        levels["Overall"] = overall_level

        self._display_final_results(user_name, language, scores, levels, overall_score, overall_level)

        if self.encryption.verify_admin():
            self.save_results(user_name, language, scores, levels)
            print("\nYour results have been saved!")
        else:
            print("\nUnable to save results - admin verification required.")

    def _display_instructions(self):
        """Display quiz instructions."""
        print("\nThis quiz will assess your skills in Reading, Writing, Speaking, and Listening.")
        print("For each statement, rate your ability from 0-5:")
        print("0 = Not at all")
        print("1 = Strongly Disagree")
        print("2 = Disagree")
        print("3 = Neutral")
        print("4 = Agree")
        print("5 = Strongly Agree\n")

    def _conduct_assessment(self):
        """Conduct the assessment for all categories."""
        scores = {}
        levels = {}
        
        for category in self.categories:
            print(f"\n{category.upper()} ASSESSMENT")
            print("-" * 50)
            print(f"Please rate your {category.lower()} abilities:\n")
            
            category_score = self._assess_category(category)
            scores[category] = category_score
            levels[category] = Levels.determine_level(category_score)
            
            print(f"\n{category} Assessment Complete!")
            print(f"Category Score: {category_score:.2f}")
            print(f"Category Level: {levels[category]}")
            print("-" * 50)
            
        return scores, levels

    def _assess_category(self, category):
        """Assess a single category and return the score."""
        category_score = 0
        
        for i, question in enumerate(self.questions[category], 1):
            while True:
                try:
                    print(f"\nQuestion {i} of {len(self.questions[category])}:")
                    response = input(f"{question['text']}\nYour rating (0-5): ")
                    response = int(response)
                    
                    if 0 <= response <= 5:
                        weighted_score = response * question['weight']
                        category_score += weighted_score
                        break
                    else:
                        print("Please enter a number between 0 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number between 0 and 5.")
                    
        return category_score

    def _display_final_results(self, user_name, language, scores, levels, overall_score, overall_level):
        """Display the final results of the assessment."""
        print("\nFINAL RESULTS")
        print("=" * 50)
        print(f"Name: {user_name}")
        print(f"Language: {language}")
        print("\nCategory Breakdown:")
        print("-" * 50)
        for category in self.categories:
            print(f"{category:10} | Score: {scores[category]:6.2f} | {levels[category]}")
        print("-" * 50)
        print(f"Overall Score: {overall_score:.2f}")
        print(f"Overall ILR Level: {overall_level}")
        print("=" * 50)
