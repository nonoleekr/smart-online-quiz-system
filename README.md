# Smart Online Quiz System (SOQS)

## Overview
The Smart Online Quiz System (SOQS) is a command-line Python application that simulates a real-world multiple-choice quiz platform. It allows users to take quizzes, receive instant feedback, and view their rankings on a dynamic leaderboard. The system is modular, with separate components for user interaction, quiz management, admin control, and utility functions. Admin Mode is password-protected and allows secure management of the quiz database (add, edit, search, delete questions in a JSON file).

## Features
- Take a 10-question multiple-choice quiz
- Instant scoring and feedback with qualitative performance assessment
- Persistent leaderboard (top scores saved, protected from tampering)
- Password-protected Admin Mode for question management
- Add, search, edit, and delete quiz questions (duplicate questions prevented)
- Modular code structure for easy maintenance

## File Structure
- `main.py` — Main entry point and menu controller
- `quiz.py` — Quiz logic (load questions, run quiz, save/view leaderboard)
- `admin.py` — Admin functions (add, search, edit, delete questions)
- `utils.py` — Utility/helper functions
- `data/questions.json` — Quiz question bank (editable)
- `data/leaderboard.json` — Leaderboard storage

## How to Run
1. Make sure you have Python 3 installed.
2. Open a terminal in the project directory.
3. Run:
   ```
   python main.py
   ```
4. Follow the on-screen menu to take a quiz, view the leaderboard, or enter Admin Mode.

## Admin Mode
- Select "Admin Mode" from the main menu.
- Enter the admin password (default: `admin123`).
- You can then add, search, edit, or delete questions in the quiz bank.
- The system prevents adding duplicate questions (case-insensitive).
- The leaderboard file is automatically set to read-only after updates to prevent tampering. Only the quiz system can write to it.

## Customization
- To change the admin password, edit the `ADMIN_PASSWORD` variable in `admin.py`.
- To add or edit questions directly, you can also modify `data/questions.json` (not recommended; use Admin Mode for validation and duplicate prevention).

## License
This project is for educational purposes.