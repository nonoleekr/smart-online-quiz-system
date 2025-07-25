# Main driver script (program entry point) 
from quiz import take_quiz, view_leaderboard
from admin import admin_mode
from utils import exit_program, clear_screen, validate_input

def main_menu():
    while True:
        clear_screen()
        print("\n")
        print_header("Main Menu")
        print("1. Take Quiz")
        print("2. View Leaderboard")
        print("3. Admin Mode")
        print("4. Exit")
        print("="*60)
        choice = validate_input("Please select an option (1-4): ", ["1", "2", "3", "4"])
        
        if choice == "1":
            take_quiz()
        elif choice == "2":
            view_leaderboard()
        elif choice == "3":
            admin_mode()
        elif choice == "4":
            exit_program()

if __name__ == "__main__":
    main_menu()