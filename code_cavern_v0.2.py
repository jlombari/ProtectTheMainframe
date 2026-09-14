import os
import time
import json
from datetime import datetime

SCORES_FILE = "scores.json"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_scores():
    """Reads saved score attempts from the JSON file."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_score(player_name, score, max_score, completed):
    """Appends a new game attempt to the JSON file."""
    scores = load_scores()
    
    new_attempt = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "name": player_name,
        "score": score,
        "max_score": max_score,
        "status": "Completed" if completed else "Defeated"
    }
    
    scores.append(new_attempt)
    
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def display_scoreboard():
    """Prints all historical attempts recorded in the file."""
    clear()
    scores = load_scores()
    
    print("========================================")
    print("           PAST ATTEMPTS LOG            ")
    print("========================================")
    
    if not scores:
        print("No recorded attempts yet!\n")
    else:
        print(f"{'Date & Time':<18} | {'Name':<12} | {'Score':<8} | {'Status'}")
        print("-" * 55)
        for attempt in reversed(scores):  # Shows newest attempts first
            date_str = attempt['date']
            name_str = attempt['name'][:12]
            score_str = f"{attempt['score']}/{attempt['max_score']}"
            status_str = attempt['status']
            print(f"{date_str:<18} | {name_str:<12} | {score_str:<8} | {status_str}")
        print("-" * 55)
    
    input("\nPress Enter to exit...")

def play_game():
    player = {"name": "", "health": 100, "score": 0}
    
    clear()
    print("========================================")
    print("   WELCOME TO THE PYTHON CODE CAVERN!   ")
    print("========================================")
    player["name"] = input("Enter your hero's name: ").strip() or "Code Ninja"
    
    questions = [
        # --- Data Types (Questions 1-5) ---
        {
            "q": "What data type is used for whole numbers like 5, 42, or 100?",
            "choices": ["1. int (Integer)", "2. str (String)", "3. float"],
            "answer": 1
        },
        {
            "q": "What data type is text inside quotes, like \"Hello World\"?",
            "choices": ["1. int", "2. str (String)", "3. bool"],
            "answer": 2
        },
        {
            "q": "Which data type can only be either True or False?",
            "choices": ["1. float", "2. int", "3. bool (Boolean)"],
            "answer": 3
        },
        {
            "q": "What data type is a decimal number like 3.14 or 9.5?",
            "choices": ["1. float", "2. str", "3. int"],
            "answer": 1
        },
        {
            "q": "What type of data does the input() function ALWAYS return?",
            "choices": ["1. int", "2. str (String)", "3. bool"],
            "answer": 2
        },
        
        # --- Variables & Printing (Questions 6-8) ---
        {
            "q": "Which Python function prints text onto the screen?",
            "choices": ["1. output()", "2. write()", "3. print()"],
            "answer": 3
        },
        {
            "q": "How do you store the value 10 inside a variable named 'score'?",
            "choices": ["1. score = 10", "2. 10 = score", "3. set score to 10"],
            "answer": 1
        },
        {
            "q": "Which variable name is written correctly in Python?",
            "choices": ["1. my score", "2. my_score", "3. 1st_score"],
            "answer": 2
        },

        # --- Math & Logic (Questions 9-11) ---
        {
            "q": "What symbol is used to check if two values are EQUAL in Python?",
            "choices": ["1. =", "2. ==", "3. ->"],
            "answer": 2
        },
        {
            "q": "What will the output of print(5 + 3 * 2) be?",
            "choices": ["1. 11", "2. 16", "3. 10"],
            "answer": 1
        },
        {
            "q": "What symbol is used for multiplication in Python?",
            "choices": ["1. x", "2. *", "3. %"],
            "answer": 2
        },

        # --- Control Flow & Loops (Questions 12-15) ---
        {
            "q": "Which keyword is used to test a condition if the first 'if' statement was False?",
            "choices": ["1. else if", "2. elif", "3. check"],
            "answer": 2
        },
        {
            "q": "Which loop runs continuously as long as a condition remains True?",
            "choices": ["1. while loop", "2. repeat loop", "3. for loop"],
            "answer": 1
        },
        {
            "q": "What symbol MUST go at the end of an 'if' or 'while' line in Python?",
            "choices": ["1. Semicolon (;)", "2. Colon (:)", "3. Period (.)"],
            "answer": 2
        },
        {
            "q": "What keyword is used to exit out of a loop early?",
            "choices": ["1. stop", "2. exit", "3. break"],
            "answer": 3
        }
    ]

    total_rooms = len(questions)
    max_possible_score = total_rooms * 10

    for idx, q in enumerate(questions, 1):
        while True:
            clear()
            print(f"Hero: {player['name']} | HP: {player['health']} | Score: {player['score']}")
            print("----------------------------------------")
            print(f"--- Cavern Room {idx} of {total_rooms} ---")
            print(q["q"] + "\n")
            for choice in q["choices"]:
                print(choice)
                
            user_choice = input("\nSelect your move (1-3): ").strip()
            
            try:
                val = int(user_choice)
                match val:
                    case 1 | 2 | 3:
                        if val == q["answer"]:
                            print("\n✨ Correct! You defeat the Code Bug!")
                            player["score"] += 10
                        else:
                            print("\n💥 Ouch! Wrong answer — the Code Bug strikes!")
                            player["health"] -= 20
                        
                        time.sleep(1.5)
                        break
                    case _:
                        input("Invalid option number! Press Enter to try again...")
            except ValueError:
                input("Please enter a valid number (1, 2, or 3)! Press Enter to try again...")
                
        # Game Over Condition
        if player["health"] <= 0:
            save_score(player['name'], player['score'], max_possible_score, completed=False)
            clear()
            print("========================================")
            print("               GAME OVER!               ")
            print("========================================")
            print(f"You ran out of HP in Room {idx}. Your attempt has been saved!")
            time.sleep(2)
            display_scoreboard()
            return

    # Victory Condition
    save_score(player['name'], player['score'], max_possible_score, completed=True)
    clear()
    print("========================================")
    print("             VICTORY! 🎉                ")
    print("========================================")
    print(f"Great job, {player['name'].upper()}! Your attempt has been saved!")
    time.sleep(2)
    display_scoreboard()

if __name__ == "__main__":
    play_game()