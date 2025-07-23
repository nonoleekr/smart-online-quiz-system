# Main driver script (program entry point) 
print("Main Menu")
print("1. Take Quiz")
print("2. View Leaderboard")
print("3. Admin Mode")
print("4. Exit")

choice = input("Please select an option (1-4): ")

if choice == "1":
    take_quiz()
elif choice == "2":
    view_leaderboard()
elif choice == "3":
    admin_mode()
elif choice == "4":
    exit_program()
else:
    print("Invalid choice. Please select a valid option.")