# Utility functions (input validation, formatting, timer, file operations)
import json
import os
import stat
import time

def exit_program():
    print("Exiting program. Goodbye!")
    exit(0)

def load_json_file(file_path):
    """Load data from a JSON file"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data
        except Exception:
            return []

def save_json_file(file_path, data, read_only=False):
    """Save data to a JSON file with optional read-only protection"""
    # Set file to writable before writing (handle cross-platform)
    if os.path.exists(file_path):
        try:
            if os.name == 'nt':
                os.chmod(file_path, stat.S_IWRITE)
            else:
                os.chmod(file_path, 0o666)
        except Exception:
            pass
            
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save data
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    # Set file to read-only after writing if requested
    if read_only:
        try:
            if os.name == 'nt':
                os.chmod(file_path, stat.S_IREAD)
            else:
                os.chmod(file_path, 0o444)
        except Exception:
            pass

def validate_input(prompt, valid_options=None, allow_empty=False):
    """Validate user input against a set of valid options"""
    while True:
        user_input = input(prompt).strip()
        
        # Check if empty input is allowed
        if not user_input and allow_empty:
            return user_input
            
        # If no valid options specified, just return non-empty input
        if valid_options is None:
            if user_input:
                return user_input
            print("Input cannot be empty. Please try again.")
            continue
            
        # Check against valid options
        if user_input.upper() in [opt.upper() for opt in valid_options]:
            return user_input.upper()
        
        # Format valid options for display
        options_str = "/".join(valid_options)
        print(f"Invalid input. Please enter one of: {options_str}")

def countdown_timer(seconds, message="Time remaining"):
    """Display a countdown timer"""
    for i in range(seconds, 0, -1):
        print(f"\r{message}: {i}s", end="")
        time.sleep(1)
    print("\rTime's up!")

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_time(seconds):
    """Format seconds into minutes and seconds"""
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}m {remaining_seconds}s"

def print_centered(text, width=60, fill_char='-'):
    """Print text centered within a line of specified width"""
    if len(text) + 2 >= width:
        print(text)
    else:
        padding = (width - len(text) - 2) // 2
        print(f"{fill_char * padding} {text} {fill_char * padding}")

def print_header(text, width=60, fill_char='='):
    """Print a header with the text centered"""
    print(fill_char * width)
    print_centered(text, width, ' ')
    print(fill_char * width)