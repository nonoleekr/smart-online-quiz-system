# Contains quiz-related logic (load, take quiz, score)
import json
import random
import os
from datetime import datetime
import threading
import sys
import time

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
    TOTAL_TIME_LIMIT = 120  # seconds for the whole quiz
    start_time = time.time()
    incorrect_answers = []
    for idx, q in enumerate(quiz_questions, 1):
        elapsed = time.time() - start_time
        if elapsed >= TOTAL_TIME_LIMIT:
            print("\nTime's up for the quiz!")
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
                if answer == q['correct_answer']:
                    print("Correct!")
                    score += 1
                else:
                    print(f"Incorrect. The correct answer is {q['correct_answer']}")
                    incorrect_answers.append({
                        'question': q['question'],
                        'user_answer': answer,
                        'correct_answer': q['correct_answer'],
                        'options': q['options']
                    })
                break
            print("Answer not valid. Please enter A, B, C, or D.")
        if (time.time() - start_time) >= TOTAL_TIME_LIMIT:
            print("\nTime's up for the quiz!")
            break
    print(f"\nQuiz complete! {name}, your score: {score}/{len(quiz_questions)}\n")
    if incorrect_answers:
        print("Here are the questions you got wrong:")
        for idx, item in enumerate(incorrect_answers, 1):
            print(f"\nQ: {item['question']}")
            for opt in item['options']:
                print(opt)
            print(f"Your answer: {item['user_answer']}")
            print(f"Correct answer: {item['correct_answer']}")
    else:
        print("Great job! You got all questions correct.")
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