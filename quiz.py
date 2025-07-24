# Contains quiz-related logic (load, take quiz, score)
import json
import random
import os
from datetime import datetime

def load_questions():
    path = os.path.join('data', 'questions.json')
    with open(path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    return questions

def save_result(name, score, total):
    path = os.path.join('data', 'leaderboard.json')
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
    # Append new result
    leaderboard.append({
        'name': name,
        'score': score,
        'total': total,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    # Save back
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(leaderboard, f, indent=2)

def take_quiz():
    questions = load_questions()
    print("\nWelcome to the Python & Computer Basics Quiz!")
    name = input("Enter your name: ").strip()
    quiz_questions = random.sample(questions, min(10, len(questions)))
    score = 0
    for idx, q in enumerate(quiz_questions, 1):
        print(f"\nQ{idx}: {q['question']}")
        for opt in q['options']:
            print(opt)
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer == q['answer']:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {q['answer']}")
    print(f"\nQuiz complete! {name}, your score: {score}/{len(quiz_questions)}\n")
    save_result(name, score, len(quiz_questions))

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
    print(f"{'Rank':<5}{'Name':<15}{'Score':<7}{'Total':<7}{'Date'}")
    for idx, entry in enumerate(leaderboard[:10], 1):
        print(f"{idx:<5}{entry['name']:<15}{entry['score']:<7}{entry['total']:<7}{entry['date']}")