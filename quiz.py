# Contains quiz-related logic (load, take quiz, score)
import random
import os
from datetime import datetime
import sys
import time
from utils import load_json_file, save_json_file, validate_input, clear_screen, print_header

def load_questions():
    path = os.path.join('data', 'questions.json')
    return load_json_file(path)

def save_result(name, score):
    path = os.path.join('data', 'leaderboard.json')
    # Load existing leaderboard
    leaderboard = load_json_file(path)
    if not isinstance(leaderboard, list):
        leaderboard = []
    
    # Append new result
    leaderboard.append({
        'name': name,
        'score': score,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    
    # Save back with read-only protection
    save_json_file(path, leaderboard, read_only=True)

def calculate_score(user_answers, quiz_questions):
    total = len(quiz_questions)
    correct = 0
    incorrect = 0
    skipped = 0
    incorrect_details = []
    for idx, (user_answer, q) in enumerate(zip(user_answers, quiz_questions)):
        if user_answer is None:
            skipped += 1
            incorrect_details.append({
                'question': q['question'],
                'user_answer': 'Skipped',
                'correct_answer': q['correct_answer'],
                'options': q['options']
            })
        elif user_answer == q['correct_answer']:
            correct += 1
        else:
            incorrect += 1
            incorrect_details.append({
                'question': q['question'],
                'user_answer': user_answer,
                'correct_answer': q['correct_answer'],
                'options': q['options']
            })
    percent = (correct / total) * 100 if total > 0 else 0
    if percent >= 90:
        feedback = 'Excellent'
    elif percent >= 70:
        feedback = 'Good'
    elif percent >= 50:
        feedback = 'Fair'
    else:
        feedback = 'Needs Improvement'
    return {
        'correct': correct,
        'incorrect': incorrect,
        'skipped': skipped,
        'total': total,
        'percent': percent,
        'feedback': feedback,
        'incorrect_details': incorrect_details
    }

def take_quiz():
    clear_screen()
    questions = load_questions()
    print_header("Python & Computer Basics Quiz")
    name = validate_input("Enter your name: ")
    quiz_questions = random.sample(questions, 10)
    user_answers = []
    TOTAL_TIME_LIMIT = 120  # seconds for the whole quiz
    start_time = time.time()
    for idx, q in enumerate(quiz_questions, 1):
        elapsed = time.time() - start_time
        if elapsed >= TOTAL_TIME_LIMIT:
            print("\nTime's up for the quiz!")
            # Mark remaining as skipped
            for _ in range(idx, 11):
                user_answers.append(None)
            break
        print(f"\nQ{idx}: {q['question']}")
        for opt in q['options']:
            print(opt)
        valid_answers = ['A', 'B', 'C', 'D']
        remaining = int(TOTAL_TIME_LIMIT - (time.time() - start_time))
        if remaining <= 0:
            print("\nTime's up for the quiz!")
            user_answer = None
        else:
            prompt = f"Your answer (A/B/C/D) [Time left: {remaining}s]: "
            answer = validate_input(prompt, valid_answers, allow_empty=True)
            user_answer = answer if answer else None
        user_answers.append(user_answer)
        if (time.time() - start_time) >= TOTAL_TIME_LIMIT:
            print("\nTime's up for the quiz!")
            # Mark remaining as skipped
            for _ in range(idx+1, 11):
                user_answers.append(None)
            break
    # Calculate score and feedback
    result = calculate_score(user_answers, quiz_questions)
    print_header("Quiz Results")
    print(f"Quiz complete! {name}, your score: {result['correct']}/10")
    print(f"Correct: {result['correct']}, Incorrect: {result['incorrect']}, Skipped: {result['skipped']}")
    print(f"Performance: {result['feedback']} ({result['percent']:.0f}%)\n")
    if result['incorrect_details']:
        print("Here are the questions you got wrong or skipped:")
        for idx, item in enumerate(result['incorrect_details'], 1):
            print(f"\nQ: {item['question']}")
            for opt in item['options']:
                print(opt)
            print(f"Your answer: {item['user_answer']}")
            print(f"Correct answer: {item['correct_answer']}")
    else:
        print("Great job! You got all questions correct.")
    save_result(name, result['correct'])
    
    # Add a pause so user can read the results
    input("\nPress Enter to continue...")

def view_leaderboard():
    clear_screen()
    print_header("Leaderboard")
    path = os.path.join('data', 'leaderboard.json')
    leaderboard = load_json_file(path)
    
    if not leaderboard:
        print("No leaderboard data found.")
        input("\nPress Enter to continue...")
        return
        
    if not isinstance(leaderboard, list):
        print("Leaderboard data is invalid.")
        input("\nPress Enter to continue...")
        return
    if not leaderboard:
        print("Leaderboard is empty.")
        input("\nPress Enter to continue...")
        return
    # Sort by score descending, then date
    leaderboard.sort(key=lambda x: (-x['score'], x['date']))
    print(f"{'Rank':<5}{'Name':<15}{'Score':<7}{'Date'}")
    print("-"*60)
    for idx, entry in enumerate(leaderboard[:10], 1):
        print(f"{idx:<5}{entry['name']:<15}{entry['score']:<7}{entry['date']}")
    
    # Add a pause so user can read the leaderboard
    input("\nPress Enter to continue...")