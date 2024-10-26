import json
from datetime import datetime
import os
import hashlib
import getpass
import base64
import secrets

class ILRQuiz:
    def __init__(self):
        self.categories = ["Reading", "Writing", "Speaking", "Listening"]
        self.questions = {
            "Reading": [
                {"text": "I can recognize a few letters or symbols.", "weight": 1, "level": "0"},
                {"text": "I can identify some high-frequency words and phrases.", "weight": 1.2, "level": "0+"},
                {"text": "I can understand basic written texts on familiar topics.", "weight": 1.5, "level": "1"},
                {"text": "I can understand routine social correspondence.", "weight": 1.7, "level": "1+"},
                {"text": "I can scan and skim texts for relevant information.", "weight": 2, "level": "2"},
                {"text": "I can understand most formal and informal texts.", "weight": 2.2, "level": "2+"},
                {"text": "I can understand abstract and linguistically complex texts.", "weight": 2.5, "level": "3"},
                {"text": "I can understand precise social and professional texts.", "weight": 2.7, "level": "3+"},
                {"text": "I can understand all styles and forms of written language.", "weight": 3, "level": "4"},
                {"text": "I can understand highly abstract concepts.", "weight": 3.2, "level": "4+"},
                {"text": "I can understand sophisticated nuances equivalent to an educated native reader.", "weight": 3.5, "level": "5"}
            ],
            "Writing": [
                {"text": "I can write a few letters or numbers.", "weight": 1, "level": "0"},
                {"text": "I can write basic personal information.", "weight": 1.2, "level": "0+"},
                {"text": "I can write simple phrases and sentences.", "weight": 1.5, "level": "1"},
                {"text": "I can write short personal notes and letters.", "weight": 1.7, "level": "1+"},
                {"text": "I can write routine social correspondence.", "weight": 2, "level": "2"},
                {"text": "I can write detailed descriptions and narratives.", "weight": 2.2, "level": "2+"},
                {"text": "I can write about complex topics clearly.", "weight": 2.5, "level": "3"},
                {"text": "I can write precise professional documents.", "weight": 2.7, "level": "3+"},
                {"text": "I can write extensively with appropriate style.", "weight": 3, "level": "4"},
                {"text": "I can write sophisticated academic papers.", "weight": 3.2, "level": "4+"},
                {"text": "I can write with sophistication equivalent to an educated native writer.", "weight": 3.5, "level": "5"}
            ],
            "Speaking": [
                {"text": "I can say a few basic words.", "weight": 1, "level": "0"},
                {"text": "I can express basic courtesies.", "weight": 1.2, "level": "0+"},
                {"text": "I can handle basic survival situations.", "weight": 1.5, "level": "1"},
                {"text": "I can participate in simple conversations.", "weight": 1.7, "level": "1+"},
                {"text": "I can function in routine social situations.", "weight": 2, "level": "2"},
                {"text": "I can discuss concrete topics with confidence.", "weight": 2.2, "level": "2+"},
                {"text": "I can participate in formal and informal conversations.", "weight": 2.5, "level": "3"},
                {"text": "I can defend opinions and hypothesize.", "weight": 2.7, "level": "3+"},
                {"text": "I can discuss complex or sensitive topics fluently.", "weight": 3, "level": "4"},
                {"text": "I can tailor language to any audience.", "weight": 3.2, "level": "4+"},
                {"text": "I can speak with sophistication equivalent to an educated native speaker.", "weight": 3.5, "level": "5"}
            ],
            "Listening": [
                {"text": "I can recognize a few basic words.", "weight": 1, "level": "0"},
                {"text": "I can understand some memorized words and phrases.", "weight": 1.2, "level": "0+"},
                {"text": "I can understand basic questions and instructions.", "weight": 1.5, "level": "1"},
                {"text": "I can understand simple conversations on familiar topics.", "weight": 1.7, "level": "1+"},
                {"text": "I can understand routine social conversations.", "weight": 2, "level": "2"},
                {"text": "I can understand most formal and informal conversations.", "weight": 2.2, "level": "2+"},
                {"text": "I can understand abstract concepts in discussions.", "weight": 2.5, "level": "3"},
                {"text": "I can understand professional discussions in my field.", "weight": 2.7, "level": "3+"},
                {"text": "I can understand all forms and styles of speech.", "weight": 3, "level": "4"},
                {"text": "I can understand highly specialized speech.", "weight": 3.2, "level": "4+"},
                {"text": "I can understand speech equivalent to an educated native listener.", "weight": 3.5, "level": "5"}
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
        self.results_file = "ilr_quiz_results.encrypted.json"
        self.admin_file = "admin_credentials.json"
        self.key = None

    def initialize_admin(self):
        """Set up admin credentials if they don't exist."""
        if not os.path.exists(self.admin_file):
            print("\nFirst-time setup: Create admin credentials")
            while True:
                admin_password = getpass.getpass("Create admin password: ")
                confirm_password = getpass.getpass("Confirm admin password: ")
                if admin_password == confirm_password:
                    salt = secrets.token_bytes(16)
                    key = hashlib.pbkdf2_hmac(
                        'sha256',
                        admin_password.encode('utf-8'),
                        salt,
                        100000
                    )
                    admin_data = {
                        'salt': base64.b64encode(salt).decode('utf-8'),
                        'key': base64.b64encode(key).decode('utf-8')
                    }
                    with open(self.admin_file, 'w') as f:
                        json.dump(admin_data, f)
                    print("Admin credentials created successfully!")
                    break
                else:
                    print("Passwords don't match. Please try again.")

    def verify_admin(self):
        """Verify admin credentials and set encryption key."""
        if not os.path.exists(self.admin_file):
            print("Admin credentials not found. Please set up first.")
            return False

        with open(self.admin_file, 'r') as f:
            admin_data = json.load(f)

        salt = base64.b64decode(admin_data['salt'])
        stored_key = base64.b64decode(admin_data['key'])

        password = getpass.getpass("Enter admin password: ")
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )

        if key == stored_key:
            self.key = key
            return True
        return False

    def encrypt_data(self, data):
        """Encrypt data using the admin key."""
        if not self.key:
            raise ValueError("Encryption key not set")
        
        # Use key as seed for simple XOR encryption (for demonstration)
        # In production, use proper encryption libraries like cryptography
        data_str = json.dumps(data)
        data_bytes = data_str.encode('utf-8')
        key_bytes = self.key * (len(data_bytes) // len(self.key) + 1)
        encrypted = bytes([a ^ b for a, b in zip(data_bytes, key_bytes)])
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt_data(self, encrypted_data):
        """Decrypt data using the admin key."""
        if not self.key:
            raise ValueError("Encryption key not set")
            
        # Reverse the XOR encryption
        encrypted_bytes = base64.b64decode(encrypted_data)
        key_bytes = self.key * (len(encrypted_bytes) // len(self.key) + 1)
        decrypted = bytes([a ^ b for a, b in zip(encrypted_bytes, key_bytes)])
        return json.loads(decrypted.decode('utf-8'))
    
    def determine_level(self, score):
        """Determine the ILR level based on the score."""
        for level in self.levels:
            if score <= level['max_score']:
                return level['name']
        return "Error: Score out of range"

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
                    results = self.decrypt_data(encrypted_data)
            else:
                results = []
            
            results.append(result)
            encrypted_results = self.encrypt_data(results)
            
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

        if not self.verify_admin():
            print("Unauthorized access. Admin authentication required.")
            return

        try:
            with open(self.results_file, 'r') as f:
                encrypted_data = f.read()
                results = self.decrypt_data(encrypted_data)

            if not results:
                print("No results found.")
                return

            if user_name:
                results = [r for r in results if r["user_name"].lower() == user_name.lower()]
                if not results:
                    print(f"No results found for user: {user_name}")
                    return

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

        except Exception as e:
            print(f"Error reading results: {e}")
            print("Please verify admin credentials and try again.")
    
    def run_quiz(self):
        """Run the ILR proficiency quiz with all questions for each category."""
        print("Welcome to the ILR Language Proficiency Self-Assessment Quiz!")
        
        user_name = input("Please enter your name: ").strip()
        language = input("Which language are you assessing? ").strip()
        
        print("\nThis quiz will assess your skills in Reading, Writing, Speaking, and Listening.")
        print("For each statement, rate your ability from 0-5:")
        print("0 = Not at all")
        print("1 = Strongly Disagree")
        print("2 = Disagree")
        print("3 = Neutral")
        print("4 = Agree")
        print("5 = Strongly Agree\n")

        scores = {}
        levels = {}
        
        for category in self.categories:
            print(f"\n{category.upper()} ASSESSMENT")
            print("-" * 50)
            print(f"Please rate your {category.lower()} abilities:\n")
            
            category_score = 0
            
            for i, question in enumerate(self.questions[category], 1):
                while True:
                    try:
                        print(f"\nQuestion {i} of {len(self.questions[category])}:")
                        response = input(f"{question['text']}\nYour rating (0-5): ")
                        response = int(response)
                        
                        if 0 <= response <= 5:  # Changed from 1-5 to 0-5
                            weighted_score = response * question['weight']
                            category_score += weighted_score
                            break
                        else:
                            print("Please enter a number between 0 and 5.")  # Updated error message
                    except ValueError:
                        print("Invalid input. Please enter a number between 0 and 5.")  # Updated error message
            
            scores[category] = category_score
            levels[category] = self.determine_level(category_score)
            
            print(f"\n{category} Assessment Complete!")
            print(f"Category Score: {category_score:.2f}")
            print(f"Category Level: {levels[category]}")
            print("-" * 50)

        overall_score = sum(scores.values()) / len(scores)
        overall_level = self.determine_level(overall_score)
        levels["Overall"] = overall_level

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

        if self.verify_admin():
            self.save_results(user_name, language, scores, levels)
            print("\nYour results have been saved!")
        else:
            print("\nUnable to save results - admin verification required.")
    
def main():
    quiz = ILRQuiz()
    quiz.initialize_admin()  # Set up admin credentials if first time
    
    while True:
        print("\nILR Language Proficiency Quiz Menu:")
        print("1. Take Quiz")
        print("2. View All Results (Admin Only)")
        print("3. View Results by Username (Admin Only)")
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