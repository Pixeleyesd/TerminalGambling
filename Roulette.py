import random
import time
import keyboard
import os
import sys

if os.name == "nt": 
    import msvcrt
else:
    import select

def clear_input_buffer():
    if os.name == "nt":
        while msvcrt.kbhit():
            msvcrt.getwch()
    else:
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()

def wait_for_key_release():
    while (
        keyboard.is_pressed("up")
        or keyboard.is_pressed("down")
        or keyboard.is_pressed("enter")
    ):
        time.sleep(0.05)

def read_menu_key():
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            return event.name

def draw_menu(title, options, player_balance, selected_index):
    print("\033c", end="")
    print("\n" + "="*30)
    print(f"--- {title} ---")
    print(f"Current Balance: ${player_balance}")
    print("="*30)
    print("Use UP and DOWN arrows to select, and ENTER to choose.\n")

    for i, option in enumerate(options):
        if i == selected_index:
            print(f"\033[7m  {option}  \033[0m")
        else:
            print(f"  {option}  ")

def get_menu_selection(title, options, player_balance):
    selected_index = 0
    clear_input_buffer()
    while True:
        draw_menu(title, options, player_balance, selected_index)
        key = read_menu_key()

        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key == "enter":
            return selected_index

def instructions_menu():
    print("\033c", end="")
    print("\n" + "="*30)
    print("--- ROULETTE INSTRUCTIONS ---")
    print("="*30)
    print("\nHow to Play:")
    print("First, choose a category to bet on:")
    print("- Numbers (0-36): Bet on a specific number.")
    print("- Colours: Bet on Red or Black.")
    print("- Odd/Even: Bet on Odd or Even numbers.")
    print("")
    print("Payouts:")
    print("- Numbers: 35x payout (e.g., bet $10, win $350).")
    print("- Colours & Odd/Even: 2x payout (e.g., bet $10, win $20).")
    print("")
    print("Note: The number 0 is Green. Bets on Red/Black")
    print("or Odd/Even will automatically lose if the ball lands on 0.")
    print("")
    
    # Wait for the enter key to be released and clear the buffer 
    # so the input doesn't trigger instantly
    wait_for_key_release()
    clear_input_buffer()
    
    input("[press enter to return to roulette menu]")
    clear_input_buffer()
    print("\033c", end="")

def play_roulette(player_balance):
    clear_input_buffer()
    
    # Roulette Main Menu
    while True:
        main_options = ["Start Roulette", "Instructions", "Back"]
        main_index = get_menu_selection("ROULETTE", main_options, player_balance)
        
        if main_index == 0:
            break
        elif main_index == 1:
            time.sleep(0.05)  #wait for key release to prevent skipping menus
            instructions_menu()
        elif main_index == 2:
            print("\033c", end="")
            return player_balance

    red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    
    # Select Bet Category
    categories = ["Numbers (0-36)", "Colours (Red/Black)", "Odd/Even", "Back"]
    cat_index = get_menu_selection("ROULETTE MENU", categories, player_balance)
    
    if cat_index == 3:
        print("\033c", end="")
        return player_balance
        
    category_choice = categories[cat_index]
    
    # select Specific Bet
    bet_target = None
    if category_choice == "Numbers (0-36)":
        print("\033c", end="")
        while True:
            clear_input_buffer()
            try:
                num = int(input("Enter a number to bet on (0-36): "))
                if 0 <= num <= 36:
                    bet_target = num
                    break
                else:
                    print("Invalid number. Must be between 0 and 36.")
            except ValueError:
                print("Please enter a valid number.")
                
    elif category_choice == "Colours (Red/Black)":
        color_options = ["Red", "Black", "Cancel"]
        col_index = get_menu_selection("SELECT COLOUR", color_options, player_balance)
        if col_index == 2:
            return player_balance
        bet_target = color_options[col_index]
        
    elif category_choice == "Odd/Even":
        parity_options = ["Odd", "Even", "Cancel"]
        par_index = get_menu_selection("SELECT ODD/EVEN", parity_options, player_balance)
        if par_index == 2:
            return player_balance
        bet_target = parity_options[par_index]

    # enter Bet Amount
    print("\033c", end="")
    while True:
        clear_input_buffer()
        try:
            bet_amount = int(input(f"Enter your bet amount on {bet_target} (Max ${player_balance}): $"))
            if 0 < bet_amount <= player_balance:
                break
            else:
                print("Invalid amount. Please bet a positive number within your balance.")
        except ValueError:
            print("Please enter a valid number.")

    # Spin the Wheel
    print("\033c", end="")
    print(f"You placed ${bet_amount} on {bet_target}.")
    print("Spinning the wheel...")

    input("\n[press enter continue]")
    
    winning_number = random.randint(0, 36)
    
    # determine attributes of the winning number
    if winning_number == 0:
        winning_color = "Green"
        winning_parity = "None"
    else:
        winning_color = "Red" if winning_number in red_numbers else "Black"
        winning_parity = "Even" if winning_number % 2 == 0 else "Odd"

    print(f"\nTHE BALL LANDED ON: {winning_number} ({winning_color})")

    # now evaluate Win/Loss
    won = False
    payout = 0

    if category_choice == "Numbers (0-36)" and bet_target == winning_number:
        won = True
        payout = bet_amount * 35  #standard roulette payout for single number
    elif category_choice == "Colours (Red/Black)" and bet_target == winning_color:
        won = True
        payout = bet_amount * 2
    elif category_choice == "Odd/Even" and bet_target == winning_parity:
        won = True
        payout = bet_amount * 2

    if won:
        winnings = payout - bet_amount
        player_balance += winnings
        print(f"\nCongratulations! You won ${winnings} (Total Payout: ${payout})!")
    else:
        player_balance -= bet_amount
        print(f"\nRip, you lost your ${bet_amount} bet.")

    clear_input_buffer()
    input("\n[press enter to return to menu]")
    clear_input_buffer()
    print("\033c", end="")
    time.sleep(0.05)  #wait for key release to prevent skipping menus.

    return player_balance