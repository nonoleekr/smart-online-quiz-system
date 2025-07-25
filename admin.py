# Admin-only features (add, search, delete questions)
import json
import os

ADMIN_PASSWORD = 'admin123'  # Change as needed
QUESTIONS_PATH = os.path.join('data', 'questions.json')

def admin_mode():
    print("\n[Admin Mode]")
    pwd = input("Enter admin password: ")
    if pwd != ADMIN_PASSWORD:
        print("Incorrect password. Returning to main menu.\n")
        return
    while True:
        print("\nAdmin Menu:")
        print("1. Add Question")
        print("2. Search Question")
        print("3. Edit Question")
        print("4. Delete Question")
        print("5. Exit Admin Mode")
        choice = input("Select an option (1-5): ")
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
        else:
            print("Invalid choice. Please select a valid option.")

def load_questions():
    if not os.path.exists(QUESTIONS_PATH):
        return []
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_questions(questions):
    with open(QUESTIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2)

def add_question():
    print("\n[Add Question]")
    question = input("Enter the question: ").strip()
    options = []
    for i in range(4):
        opt = input(f"Enter option {chr(65+i)}: ").strip()
        options.append(f"{chr(65+i)}. {opt}")
    answer = input("Enter the correct answer (A/B/C/D): ").strip().upper()
    if answer not in ['A', 'B', 'C', 'D']:
        print("Invalid answer. Must be A, B, C, or D.")
        return
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
    print("\n[Search Question]")
    keyword = input("Enter keyword to search: ").strip().lower()
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

def edit_question():
    print("\n[Edit Question]")
    questions = load_questions()
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q['question']}")
    try:
        num = int(input("Enter the number of the question to edit: "))
        if not (1 <= num <= len(questions)):
            print("Invalid question number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    q = questions[num-1]
    print(f"Current question: {q['question']}")
    new_q = input("Enter new question (leave blank to keep current): ").strip()
    if new_q:
        q['question'] = new_q
    for i in range(4):
        print(f"Current option {chr(65+i)}: {q['options'][i]}")
        new_opt = input(f"Enter new option {chr(65+i)} (leave blank to keep current): ").strip()
        if new_opt:
            q['options'][i] = f"{chr(65+i)}. {new_opt}"
    new_ans = input(f"Enter new correct answer (A/B/C/D, leave blank to keep {q['correct_answer']}): ").strip().upper()
    if new_ans in ['A', 'B', 'C', 'D']:
        q['correct_answer'] = new_ans
    save_questions(questions)
    print("Question updated successfully!\n")

def delete_question():
    print("\n[Delete Question]")
    questions = load_questions()
    for idx, q in enumerate(questions, 1):
        print(f"{idx}. {q['question']}")
    try:
        num = int(input("Enter the number of the question to delete: "))
        if not (1 <= num <= len(questions)):
            print("Invalid question number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    confirm = input(f"Are you sure you want to delete this question? (y/n): ").strip().lower()
    if confirm == 'y':
        del questions[num-1]
        save_questions(questions)
        print("Question deleted successfully!\n")
    else:
        print("Deletion cancelled.\n")