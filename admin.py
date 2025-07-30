# Admin-only features (add, search, delete questions)
import os
from utils import load_json_file, save_json_file, validate_input, clear_screen, print_header

ADMIN_PASSWORD = 'admin123'  # Change as needed
QUESTIONS_PATH = os.path.join('data', 'questions.json')
def admin_mode():
    clear_screen()
    print_header("Admin Mode")
    pwd = validate_input("Enter admin password: ")
    if pwd != ADMIN_PASSWORD:
        print("Incorrect password. Returning to main menu.\n")
        return
    while True:
        clear_screen()
        print_header("Admin Menu")
        print("1. Add Question")
        print("2. Search Question")
        print("3. Edit Question")
        print("4. Delete Question")
        print("5. Exit Admin Mode")
        print("="*60)
        choice = validate_input("Select an option (1-5): ", ["1", "2", "3", "4", "5"])
        
        if choice == "1":
            add_question()
        elif choice == "2":
            search_question()
        elif choice == "3":
            edit_question()
        elif choice == "4":
            delete_question()
        elif choice == "5":
            print("Exiting Admin Mode.\n")
            break

def load_questions():
    return load_json_file(QUESTIONS_PATH)

def save_questions(questions):
    save_json_file(QUESTIONS_PATH, questions)

def add_question():
    clear_screen()
    print_header("Add Question")  
    question = validate_input("Enter the question: ")
    options = []
    for i in range(4):
        opt = validate_input(f"Enter option {chr(65+i)}: ")
        options.append(f"{chr(65+i)}. {opt}")
    answer = validate_input("Enter the correct answer (A/B/C/D): ", ["A", "B", "C", "D"])
    questions = load_questions()
    # Duplicate prevention: check if question text already exists
    for q in questions:
        if q['question'].strip().lower() == question.lower():
            print("This question already exists in the database. Not adding duplicate.")
            return
    questions.append({
        'question': question,
        'options': options,
        'correct_answer': answer
    })
    save_questions(questions)
    print("Question added successfully!\n")

def search_question():
    clear_screen()
    print_header("Search Question")
    keyword = validate_input("Enter keyword to search: ").lower()
    questions = load_questions()
    found = False
    for idx, q in enumerate(questions, 1):
        if keyword in q['question'].lower():
            print(f"\nQ{idx}: {q['question']}")
            for opt in q['options']:
                print(opt)
            print(f"Answer: {q['correct_answer']}")
            found = True
    if not found:
        print("No questions found with that keyword.\n")
    
    # Add a pause so user can read the search results
    input("\nPress Enter to continue...")

def edit_question():
    clear_screen()
    print_header("Edit Question")
    questions = load_questions()
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q['question']}")
    try:
        num = int(validate_input("Enter the number of the question to edit: "))
        if not (1 <= num <= len(questions)):
            print("Invalid question number.")
            input("\nPress Enter to continue...")
            return
    except ValueError:
        print("Invalid input.")
        input("\nPress Enter to continue...")
        return
    q = questions[num-1]
    print(f"Current question: {q['question']}")
    new_q = validate_input("Enter new question (leave blank to keep current): ")
    if new_q:
        q['question'] = new_q
    for i in range(4):
        print(f"Current option {chr(65+i)}: {q['options'][i]}")
        new_opt = validate_input(f"Enter new option {chr(65+i)} (leave blank to keep current): ")
        if new_opt:
            q['options'][i] = f"{chr(65+i)}. {new_opt}"
    new_ans = validate_input(f"Enter new correct answer (A/B/C/D, leave blank to keep {q['correct_answer']}): ")
    if new_ans.upper() in ['A', 'B', 'C', 'D']:
        q['correct_answer'] = new_ans.upper()
    save_questions(questions)
    print("Question updated successfully!\n")
    input("\nPress Enter to continue...")

def delete_question():
    clear_screen()
    print_header("Delete Question")
    questions = load_questions()
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q['question']}")
    try:
        num = int(validate_input("Enter the number of the question to delete: "))
        if not (1 <= num <= len(questions)):
            print("Invalid question number.")
            input("\nPress Enter to continue...")
            return
    except ValueError:
        print("Invalid input.")
        input("\nPress Enter to continue...")
        return
    confirm = validate_input(f"Are you sure you want to delete this question? (y/n): ", ["y", "n"])
    if confirm.upper() == 'Y':
        del questions[num-1]
        save_questions(questions)
        print("Question deleted successfully!")
    else:
        print("Deletion cancelled.")
    input("\nPress Enter to continue...")