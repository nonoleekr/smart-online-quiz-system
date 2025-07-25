# Contains quiz-related logic (load, take quiz, score)
import json
import random
import os
from datetime import datetime
import threading
import sys
import time
import stat

def load_questions():
    path = os.path.join('data', 'questions.json')
    with open(path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return questions

def save_result(name, score):
    path = os.path.join('data', 'leaderboard.json')
    # Set file to writable before writing (handle cross-platform)
    if os.path.exists(path):
        try:
            if os.name == 'nt':
                os.chmod(path, stat.S_IWRITE)
            else:
                os.chmod(path, 0o666)
        except Exception:
            pass
    # Load existing leaderboard
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    leaderboard = data
                else:
                    leaderboard = []
            except Exception:
                leaderboard = []
    else:
        leaderboard = []
    # Append new result (no 'total')
    leaderboard.append({
        'name': name,
        'score': score,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    # Save back
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, indent=2)
    # Set file to read-only after writing (handle cross-platform)
    try:
        if os.name == 'nt':
            os.chmod(path, stat.S_IREAD)
        else:
            os.chmod(path, 0o444)
    except Exception:
        pass

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
    questions = load_questions()
    print("\nWelcome to the Python & Computer Basics Quiz!")
    name = input("Enter your name: ").strip()
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
        valid_answers = {'A', 'B', 'C', 'D'}
        user_answer = None
        while True:
            remaining = int(TOTAL_TIME_LIMIT - (time.time() - start_time))
            if remaining <= 0:
                print("\nTime's up for the quiz!")
                break
            answer = input(f"Your answer (A/B/C/D) [Time left: {remaining}s]: ").strip().upper()
            if answer in valid_answers:
                user_answer = answer
                break
            elif answer == '':
                user_answer = None
                break
            print("Answer not valid. Please enter A, B, C, or D.")
        user_answers.append(user_answer)
        if (time.time() - start_time) >= TOTAL_TIME_LIMIT:
            print("\nTime's up for the quiz!")
            # Mark remaining as skipped
            for _ in range(idx+1, 11):
                user_answers.append(None)
            break
    # Calculate score and feedback
    result = calculate_score(user_answers, quiz_questions)
    print("--------------------------------")
    print(f"\nQuiz complete! {name}, your score: {result['correct']}/10")
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

def view_leaderboard():
    path = os.path.join('data', 'leaderboard.json')
    if not os.path.exists(path):
        print("No leaderboard data found.")
        return
    with open(path, 'r', encoding='utf-8') as f:
        try:
            leaderboard = json.load(f)
            if not isinstance(leaderboard, list):
                print("Leaderboard data is invalid.")
                return
        except Exception:
            print("Leaderboard data is invalid.")
            return
    if not leaderboard:
        print("Leaderboard is empty.")
        return
    # Sort by score descending, then date
    leaderboard.sort(key=lambda x: (-x['score'], x['date']))
    print("\nLeaderboard:")
    print(f"{'Rank':<5}{'Name':<15}{'Score':<7}{'Date'}")
    for idx, entry in enumerate(leaderboard[:10], 1):
        print(f"{idx:<5}{entry['name']:<15}{entry['score']:<7}{entry['date']}")