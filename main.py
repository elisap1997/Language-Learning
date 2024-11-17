# main.py
from quiz import ILRQuiz

def main():
    quiz = ILRQuiz()
    quiz.encryption.initialize_admin()
    
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