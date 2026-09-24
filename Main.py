import json
import os
import time
import keyboard
from HorseRacing import play_horse_race


SAVE_FILE = "saves.json"
STARTING_BALANCE = 200


def load_saves(): #this was taken from stackoverflow, starting here
    if not os.path.exists(SAVE_FILE):
        return {}
    with open(SAVE_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


def save_data(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4) #this was taken from stackoverflow, ending here


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') #google AI overview gave this to me for linux and windows compatibility but ik how this works


def wait_for_key_release():
    while keyboard.is_pressed("up") or keyboard.is_pressed("down") or keyboard.is_pressed("enter"):
        time.sleep(0.05) #you need these time.sleeps to prevent the program from skipping menus, otherwise it will skip the menu if you hold down a key for too long


def get_leaderboard(data):
    if not data:
        return "No entries yet."
    
    # Sort by money in descending order
    sorted_players = sorted(data.items(), key=lambda item: item[1], reverse=True)
    
    leaderboard_text = "--- LEADERBOARD ---\n"
    for rank, (name, money) in enumerate(sorted_players, start=1):
        leaderboard_text += f"{rank}. {name}: ${money}\n"
    return leaderboard_text


def main_menu(player_name, data):
    options = ["Play Horse Race", "Exit"]
    selected_index = 0

    while True:
        clear_screen()
        print(f"Welcome, {player_name}! Current Balance: ${data[player_name]}")
        print("Use UP and DOWN arrows to select, and ENTER to choose.\n")
        
        # Print menu with highlights
        for i, option in enumerate(options):
            if i == selected_index:
                print(f"\033[7m  {option}  \033[0m")
            else:
                print(f"  {option}  ")
                
        print("\n" + get_leaderboard(data))

        # Wait for key release to prevent skipping menus
        time.sleep(0.05)
        
        while True:
            if keyboard.is_pressed("up"):
                selected_index = (selected_index - 1) % len(options)
                wait_for_key_release()
                break

            elif keyboard.is_pressed("down"):
                selected_index = (selected_index + 1) % len(options)
                wait_for_key_release()
                break

            elif keyboard.is_pressed("enter"):
                wait_for_key_release()
                return selected_index


def main():
    clear_screen()
    data = load_saves()
    
    print("Welcome to Gambling!")
    player_name = input("Enter your name: ").strip()
    
    if not player_name:
        print("Name cannot be empty.")
        return

    # Create new save or load existing
    if player_name not in data:
        data[player_name] = STARTING_BALANCE
        save_data(data)
        print(f"New save created. Starting balance: ${STARTING_BALANCE}")
    else:
        print(f"Save loaded. Current balance: ${data[player_name]}")
    
    time.sleep(0.05)# Wait for key release to prevent skipping menus

    # main application loop
    while True:
        choice = main_menu(player_name, data)
        wait_for_key_release()
        
        if choice == 0: # play horse gameee
            clear_screen()

            # run the race and update balance
            new_balance = play_horse_race(data[player_name])
            data[player_name] = new_balance
            
            # check for bankruptcy
            if data[player_name] <= 0:
                clear_screen()
                print("You ran out of money, your save has been deleted.")
                del data[player_name] #this makes it so that if you run out of money, your save is deleted so you aren't softlocked.
                save_data(data)
                break
            else:
                save_data(data)
                
        elif choice == 1: # exit
            clear_screen()
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()